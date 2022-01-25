from typing import Union

from libcst import (
    BaseExpression,
    BaseSmallStatement,
    BaseStatement,
    Call,
    ClassDef,
    FlattenSentinel,
    FunctionDef,
    ImportFrom,
    ImportStar,
    Module,
    RemovalSentinel,
)
from libcst import matchers as m

from django_codemod.constants import DJANGO_1_3, DJANGO_2_1, DJANGO_3_0, DJANGO_3_1
from django_codemod.utils.calls import parse_arg, parse_param
from django_codemod.visitors.base import (
    BaseDjCodemodTransformer,
    BaseRenameTransformer,
    module_matcher,
)


class InlineHasAddPermissionsTransformer(BaseDjCodemodTransformer):
    """Add the `obj` argument to `InlineModelAdmin.has_add_permission()`."""

    deprecated_in = DJANGO_2_1
    removed_in = DJANGO_3_0
    ctx_key_prefix = "InlineHasAddPermissionsTransformer"
    ctx_key_base_cls_matcher = f"{ctx_key_prefix}-base_cls_matcher"
    ctx_key_visiting_subclass = f"{ctx_key_prefix}-is_visiting_subclass"

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[
        BaseSmallStatement, FlattenSentinel[BaseSmallStatement], RemovalSentinel
    ]:
        if isinstance(updated_node.names, ImportStar):
            return super().leave_ImportFrom(original_node, updated_node)
        base_cls_matcher = []
        if m.matches(
            updated_node,
            m.ImportFrom(module=module_matcher(["django", "contrib", "admin"])),
        ):
            for imported_name in updated_node.names:
                if m.matches(
                    imported_name, m.ImportAlias(name=m.Name("TabularInline"))
                ):
                    base_cls_matcher.append(m.Arg(m.Name("TabularInline")))
                if m.matches(
                    imported_name, m.ImportAlias(name=m.Name("StackedInline"))
                ):
                    base_cls_matcher.append(m.Arg(m.Name("StackedInline")))
        if m.matches(
            updated_node,
            m.ImportFrom(module=module_matcher(["django", "contrib"])),
        ):
            for imported_name in updated_node.names:
                if m.matches(imported_name, m.ImportAlias(name=m.Name("admin"))):

                    base_cls_matcher.extend(
                        [
                            m.Arg(
                                m.Attribute(
                                    value=m.Name("admin"), attr=m.Name("TabularInline")
                                )
                            ),
                            m.Arg(
                                m.Attribute(
                                    value=m.Name("admin"), attr=m.Name("StackedInline")
                                )
                            ),
                        ]
                    )
        # Save valid matchers in the context
        if base_cls_matcher:
            self.context.scratch[self.ctx_key_base_cls_matcher] = m.OneOf(
                *base_cls_matcher
            )
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Module(self, original_node: Module, updated_node: Module) -> Module:
        self.context.scratch.pop(self.ctx_key_base_cls_matcher, None)
        return super().leave_Module(original_node, updated_node)

    @property
    def base_cls_matcher(self):
        return self.context.scratch.get(self.ctx_key_base_cls_matcher)

    def visit_ClassDef_bases(self, node: ClassDef) -> None:
        if self.base_cls_matcher is not None:
            for base_cls in node.bases:
                if m.matches(base_cls, self.base_cls_matcher):
                    self.context.scratch[self.ctx_key_visiting_subclass] = True
        super().visit_ClassDef_bases(node)

    def leave_ClassDef(
        self, original_node: ClassDef, updated_node: ClassDef
    ) -> Union[BaseStatement, FlattenSentinel[BaseStatement], RemovalSentinel]:
        self.context.scratch.pop(self.ctx_key_visiting_subclass, None)
        return super().leave_ClassDef(original_node, updated_node)

    @property
    def is_visiting_subclass(self):
        return self.context.scratch.get(self.ctx_key_visiting_subclass, False)

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> Union[BaseStatement, FlattenSentinel[BaseStatement], RemovalSentinel]:
        if (
            self.is_visiting_subclass
            and m.matches(
                updated_node, m.FunctionDef(name=m.Name("has_add_permission"))
            )
            and len(updated_node.params.params) == 2
        ):
            old_params = updated_node.params
            updated_params = old_params.with_changes(
                params=(
                    *old_params.params,
                    parse_param("obj=None"),
                )
            )
            return updated_node.with_changes(params=updated_params)
        return super().leave_FunctionDef(original_node, updated_node)

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if (
            self.is_visiting_subclass
            and m.matches(
                updated_node,
                m.Call(
                    func=m.Attribute(
                        attr=m.Name("has_add_permission"),
                        value=m.Call(func=m.Name("super")),
                    )
                ),
            )
            and len(updated_node.args) < 2
        ):
            updated_args = (
                *updated_node.args,
                parse_arg("obj=obj"),
            )
            return updated_node.with_changes(args=updated_args)
        return super().leave_Call(original_node, updated_node)


class ActionCheckboxNameTransformer(BaseRenameTransformer):
    """Replace `django.contrib.admin.ACTION_CHECKBOX_NAME` compatibility import"""

    deprecated_in = DJANGO_1_3
    removed_in = DJANGO_3_1
    rename_from = "django.contrib.admin.ACTION_CHECKBOX_NAME"
    rename_to = "django.contrib.admin.helpers.ACTION_CHECKBOX_NAME"
