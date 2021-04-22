from typing import Optional, Sequence, Union

from libcst import (
    Arg,
    BaseExpression,
    BaseSmallStatement,
    BaseStatement,
    Call,
    FlattenSentinel,
    FunctionDef,
    ImportFrom,
    ImportStar,
    MaybeSentinel,
    Name,
    RemovalSentinel,
    RemoveFromParent,
    Return,
)
from libcst import matchers as m
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import (
    DJANGO_1_9,
    DJANGO_1_11,
    DJANGO_2_0,
    DJANGO_2_1,
    DJANGO_3_1,
    DJANGO_4_0,
)
from django_codemod.utils.calls import find_keyword_arg, parse_arg
from django_codemod.visitors.base import (
    BaseDjCodemodTransformer,
    BaseFuncRenameTransformer,
    module_matcher,
)


class ModelsPermalinkTransformer(BaseDjCodemodTransformer):
    """Replace `@models.permalink` decorator by a call to `reverse()`."""

    deprecated_in = DJANGO_1_11
    removed_in = DJANGO_2_1
    ctx_key_prefix = "ModelsPermalinkTransformer"
    ctx_key_inside_method = f"{ctx_key_prefix}-inside_method"
    ctx_key_decorator_matchers = f"{ctx_key_prefix}-decorator_matchers"

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[
        BaseSmallStatement, FlattenSentinel[BaseSmallStatement], RemovalSentinel
    ]:
        if isinstance(updated_node.names, ImportStar):
            return super().leave_ImportFrom(original_node, updated_node)
        if m.matches(
            updated_node,
            m.ImportFrom(module=module_matcher(["django", "db"])),
        ):
            for imported_name in updated_node.names:
                if m.matches(imported_name, m.ImportAlias(name=m.Name("models"))):
                    self.add_decorator_matcher(
                        m.Decorator(
                            decorator=m.Attribute(
                                value=m.Name("models"), attr=m.Name("permalink")
                            )
                        )
                    )
        if m.matches(
            updated_node,
            m.ImportFrom(module=module_matcher(["django", "db", "models"])),
        ):
            updated_names = []
            for imported_name in updated_node.names:
                if m.matches(imported_name, m.ImportAlias(name=m.Name("permalink"))):
                    decorator_name_str = (
                        imported_name.evaluated_alias or imported_name.evaluated_name
                    )
                    self.add_decorator_matcher(
                        m.Decorator(decorator=m.Name(decorator_name_str))
                    )
                else:
                    updated_names.append(imported_name)
            if not updated_names:
                return RemoveFromParent()
            # sort imports
            new_names = sorted(updated_names, key=lambda n: n.evaluated_name)
            # remove any trailing commas
            last_name = new_names[-1]
            if last_name.comma != MaybeSentinel.DEFAULT:
                new_names[-1] = last_name.with_changes(comma=MaybeSentinel.DEFAULT)
            return updated_node.with_changes(names=new_names)
        return super().leave_ImportFrom(original_node, updated_node)

    def add_decorator_matcher(self, matcher):
        if self.ctx_key_decorator_matchers not in self.context.scratch:
            self.context.scratch[self.ctx_key_decorator_matchers] = []
        self.context.scratch[self.ctx_key_decorator_matchers].append(matcher)

    @property
    def decorator_matcher(self):
        matchers_list = self.context.scratch.get(self.ctx_key_decorator_matchers, [])
        if len(matchers_list) == 0:
            return None
        if len(matchers_list) == 1:
            return matchers_list[0]
        return m.OneOf(*[matcher for matcher in matchers_list])

    def visit_FunctionDef(self, node: FunctionDef) -> Optional[bool]:
        for decorator in node.decorators:
            if m.matches(decorator, self.decorator_matcher):
                self.context.scratch[self.ctx_key_inside_method] = True
        return super().visit_FunctionDef(node)

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> Union[BaseStatement, FlattenSentinel[BaseStatement], RemovalSentinel]:
        if self.visiting_permalink_method:
            for decorator in updated_node.decorators:
                if m.matches(decorator, self.decorator_matcher):
                    AddImportsVisitor.add_needed_import(
                        context=self.context,
                        module="django.urls",
                        obj="reverse",
                    )
                    updated_decorators = list(updated_node.decorators)
                    updated_decorators.remove(decorator)
                    self.context.scratch.pop(self.ctx_key_inside_method, None)
                    return updated_node.with_changes(
                        decorators=tuple(updated_decorators)
                    )
        return super().leave_FunctionDef(original_node, updated_node)

    @property
    def visiting_permalink_method(self):
        return self.context.scratch.get(self.ctx_key_inside_method, False)

    def leave_Return(
        self, original_node: Return, updated_node: Return
    ) -> Union[
        BaseSmallStatement, FlattenSentinel[BaseSmallStatement], RemovalSentinel
    ]:
        if self.visiting_permalink_method and m.matches(
            updated_node.value, m.Tuple()  # type: ignore
        ):
            elem_0, *elem_1_3 = updated_node.value.elements[:3]  # type: ignore
            args = (
                Arg(elem_0.value),
                Arg(Name("None")),
                *[Arg(el.value) for el in elem_1_3],
            )
            return updated_node.with_changes(
                value=Call(func=Name("reverse"), args=args)
            )
        return super().leave_Return(original_node, updated_node)


def is_foreign_key(node: Call) -> bool:
    return m.matches(node, m.Call(func=m.Attribute(attr=m.Name(value="ForeignKey"))))


def is_one_to_one_field(node: Call) -> bool:
    return m.matches(
        node,
        m.Call(func=m.Attribute(attr=m.Name(value="OneToOneField"))),
    )


def has_on_delete(node: Call) -> bool:
    # if on_delete exists in any kwarg we return True
    if find_keyword_arg(node.args, "on_delete"):
        return True

    # if there are two or more nodes and there are no keywords
    # then we can assume that positional arguments are being used
    # and on_delete is being handled.
    return len(node.args) >= 2 and node.args[1].keyword is None


class OnDeleteTransformer(BaseDjCodemodTransformer):
    """Add the `on_delete=CASCADE` to `ForeignKey` and `OneToOneField`."""

    deprecated_in = DJANGO_1_9
    removed_in = DJANGO_2_0
    ctx_key_prefix = "OnDeleteTransformer"

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if (
            is_one_to_one_field(original_node) or is_foreign_key(original_node)
        ) and not has_on_delete(original_node):
            AddImportsVisitor.add_needed_import(
                context=self.context,
                module="django.db",
                obj="models",
            )
            updated_args = (
                *updated_node.args,
                parse_arg("on_delete=models.CASCADE"),
            )
            return updated_node.with_changes(args=updated_args)
        return super().leave_Call(original_node, updated_node)


class NullBooleanFieldTransformer(BaseFuncRenameTransformer):
    """Replace `NullBooleanField` by `BooleanField` with `null=True`."""

    deprecated_in = DJANGO_3_1
    removed_in = DJANGO_4_0

    rename_from = "django.db.models.NullBooleanField"
    rename_to = "django.db.models.BooleanField"

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return (
            *node.args,
            parse_arg("null=True"),
        )
