from typing import Union

from libcst import (
    BaseSmallStatement,
    BaseStatement,
    ClassDef,
    FunctionDef,
    ImportFrom,
    Module,
    Name,
    Param,
    RemovalSentinel,
)
from libcst import matchers as m
from libcst.codemod import ContextAwareTransformer

from django_codemod.constants import DJANGO_21, DJANGO_30
from django_codemod.visitors.base import module_matcher


class InlineHasAddPermissionsTransformer(ContextAwareTransformer):
    """Add the ``obj`` argument to ``InlineModelAdmin.has_add_permission()``."""

    deprecated_in = DJANGO_21
    removed_in = DJANGO_30
    context_key = "InlineHasAddPermissionsTransformer"

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
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
            updated_node, m.ImportFrom(module=module_matcher(["django", "contrib"])),
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
            self.context.scratch[f"{self.context_key}-base_cls_matcher"] = m.OneOf(
                *base_cls_matcher
            )
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Module(self, original_node: Module, updated_node: Module) -> Module:
        self.context.scratch.pop(f"{self.context_key}-base_cls_matcher", None)
        return super().leave_Module(original_node, updated_node)

    @property
    def base_cls_matcher(self):
        return self.context.scratch.get(f"{self.context_key}-base_cls_matcher")

    def visit_ClassDef_bases(self, node: ClassDef) -> None:
        if self.base_cls_matcher is not None:
            for base_cls in node.bases:
                if m.matches(base_cls, self.base_cls_matcher):
                    self.context.scratch[
                        f"{self.context_key}-is_visiting_subclass"
                    ] = True
        super().visit_ClassDef_bases(node)

    def leave_ClassDef(
        self, original_node: ClassDef, updated_node: ClassDef
    ) -> Union[BaseStatement, RemovalSentinel]:
        self.context.scratch.pop(f"{self.context_key}-is_visiting_subclass", None)
        return super().leave_ClassDef(original_node, updated_node)

    @property
    def is_visiting_subclass(self):
        return self.context.scratch.get(
            f"{self.context_key}-is_visiting_subclass", False
        )

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> Union[BaseStatement, RemovalSentinel]:
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
                    Param(name=Name("obj"), default=Name("None")),
                )
            )
            return updated_node.with_changes(params=updated_params)
        return super().leave_FunctionDef(original_node, updated_node)
