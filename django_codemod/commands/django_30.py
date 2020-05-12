# This is expected to cover most of the things listed in this section:
# https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-0
from typing import Sequence

from libcst import Call, Name, Arg

from django_codemod.commands.base import BaseSimpleFuncRename


class RenderToResponseToRenderCommand(BaseSimpleFuncRename):
    """
    Resolve deprecation of ``django.shortcuts.render_to_response``.

    Replaces ``render_to_response()`` by ``render()`` and add
    ``request=None`` as the first argument of ``render()``.
    """

    DESCRIPTION: str = "Replaces render_to_response() by render()."
    rename_from = "django.shortcuts.render_to_response"
    rename_to = "django.shortcuts.render"

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return (Arg(value=Name("None")), *node.args)
