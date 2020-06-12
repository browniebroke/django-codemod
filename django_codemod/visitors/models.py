from typing import Optional, Union

from libcst import (
    Arg,
    BaseSmallStatement,
    BaseStatement,
    Call,
    FunctionDef,
    ImportFrom,
    Name,
    RemovalSentinel,
    RemoveFromParent,
    Return,
)
from libcst import matchers as m
from libcst.codemod import ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import DJANGO_21, DJANGO_111
from django_codemod.visitors.base import module_matcher


class ModelsPermalinkTransformer(ContextAwareTransformer):
    """Replaces ``@models.permalink`` decorator by its equivalent."""

    deprecated_in = DJANGO_111
    removed_in = DJANGO_21
    ctx_key_prefix = "ModelsPermalinkTransformer"
    ctx_key_inside_method = f"{ctx_key_prefix}-inside_method"
    ctx_key_decorator_matchers = f"{ctx_key_prefix}-decorator_matchers"

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if m.matches(
            updated_node, m.ImportFrom(module=module_matcher(["django", "db"])),
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
                    self.add_decorator_matcher(
                        m.Decorator(decorator=m.Name("permalink"))
                    )
                else:
                    updated_names.append(imported_name)
            if not updated_names:
                return RemoveFromParent()
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
    ) -> Union[BaseStatement, RemovalSentinel]:
        if self.visiting_permalink_method:
            for decorator in updated_node.decorators:
                if m.matches(decorator, self.decorator_matcher):
                    AddImportsVisitor.add_needed_import(
                        context=self.context, module="django.urls", obj="reverse",
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
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if self.visiting_permalink_method and m.matches(updated_node.value, m.Tuple()):
            elem_0 = updated_node.value.elements[0]
            elem_1_3 = updated_node.value.elements[1:3]
            args = (
                Arg(elem_0.value),
                Arg(Name("None")),
                *[Arg(el.value) for el in elem_1_3],
            )
            return updated_node.with_changes(
                value=Call(func=Name("reverse"), args=args)
            )
        return super().leave_Return(original_node, updated_node)
