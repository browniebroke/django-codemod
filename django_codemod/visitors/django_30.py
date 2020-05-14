# This is expected to cover most of the things listed in this section:
# https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-0
from typing import Sequence, Union

from libcst import (
    Call,
    Name,
    Arg,
    RemovalSentinel,
    matchers as m,
    ClassDef,
    BaseStatement,
    FunctionDef,
    Param,
)
from libcst.codemod import ContextAwareTransformer

from .base import BaseSimpleFuncRenameTransformer


class RenderToResponseToRenderTransformer(BaseSimpleFuncRenameTransformer):
    """
    Resolve deprecation of ``django.shortcuts.render_to_response``.

    Replaces ``render_to_response()`` by ``render()`` and add
    ``request=None`` as the first argument of ``render()``.
    """

    rename_from = "django.shortcuts.render_to_response"
    rename_to = "django.shortcuts.render"

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return (Arg(value=Name("None")), *node.args)


class InlineHasAddPermissionsTransformer(ContextAwareTransformer):
    """Add the ``obj`` argument to ``InlineModelAdmin.has_add_permission()``."""

    context_key = "InlineHasAddPermissionsTransformer"

    def visit_ClassDef_bases(self, node: ClassDef) -> None:
        if m.matches(
            node,
            m.ClassDef(
                bases=(
                    m.OneOf(
                        m.Arg(
                            m.Attribute(
                                value=m.Name("admin"), attr=m.Name("TabularInline")
                            )
                        ),
                        m.Arg(m.Name("TabularInline")),
                        m.Arg(
                            m.Attribute(
                                value=m.Name("admin"), attr=m.Name("StackedInline")
                            )
                        ),
                        m.Arg(m.Name("StackedInline")),
                    ),
                )
            ),
        ):
            self.context.scratch[self.context_key] = True
        super().visit_ClassDef_bases(node)

    def leave_ClassDef(
        self, original_node: ClassDef, updated_node: ClassDef
    ) -> Union[BaseStatement, RemovalSentinel]:
        self.context.scratch.pop(self.context_key, None)
        return super().leave_ClassDef(original_node, updated_node)

    @property
    def _is_context_right(self):
        return self.context.scratch.get(self.context_key, False)

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> Union[BaseStatement, RemovalSentinel]:
        if (
            m.matches(updated_node, m.FunctionDef(name=m.Name("has_add_permission")))
            and self._is_context_right
        ):
            if len(updated_node.params.params) == 2:
                old_params = updated_node.params
                updated_params = old_params.with_changes(
                    params=(
                        *old_params.params,
                        Param(name=Name("obj"), default=Name("None")),
                    )
                )
                return updated_node.with_changes(params=updated_params)
        return super().leave_FunctionDef(original_node, updated_node)
