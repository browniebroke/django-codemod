"""
Module to fix things removed in Django 3.0.

This is expected to cover most of the things listed in this section:
https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-0
"""
from libcst import ImportFrom, Call, BaseExpression, Name, Arg
from libcst import matchers as m
from django_codemod.commands.base import BaseSimpleFuncRename


class RenderToResponseToRenderCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.shortcuts.render_to_response."""

    DESCRIPTION: str = "Replaces render_to_response() by render()."
    old_name = "render_to_response"
    new_name = "render"

    def _test_import_from(self, node: ImportFrom) -> bool:
        return m.matches(
            node,
            m.ImportFrom(
                module=m.Attribute(value=m.Name("django"), attr=m.Name("shortcuts")),
            ),
        )

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if m.matches(updated_node, m.Call(func=m.Name(self.old_name))):
            updated_args = (
                Arg(value=Name("None")),
                *updated_node.args,
            )
            return Call(args=updated_args, func=Name(self.new_name))
        return super().leave_Call(original_node, updated_node)
