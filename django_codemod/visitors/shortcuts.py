from typing import Sequence

from libcst import Arg, Call, Name

from django_codemod.constants import DJANGO_2_0, DJANGO_3_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class RenderToResponseTransformer(BaseFuncRenameTransformer):
    """
    Replace `render_to_response()` by `render()`.

    Use `None` as the first argument to `render()`.
    """

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0
    rename_from = "django.shortcuts.render_to_response"
    rename_to = "django.shortcuts.render"

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return (Arg(value=Name("None")), *node.args)
