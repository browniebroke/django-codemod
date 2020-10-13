from typing import Sequence

from libcst import Arg, Call, Integer

from django_codemod.constants import DJANGO_3_1, DJANGO_4_0
from django_codemod.utils.calls import find_keyword_arg
from django_codemod.visitors.base import BaseFuncRenameTransformer


class GetRandomStringTransformer(BaseFuncRenameTransformer):
    """Update lengthless uses of get_random_string()"""

    deprecated_in = DJANGO_3_1
    removed_in = DJANGO_4_0
    rename_from = "django.utils.crypto.get_random_string"
    rename_to = "django.utils.crypto.get_random_string"

    # The default value Django specifies is 12.
    default_length_value = Integer("12")

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        # No args? Just add the default 12.
        if not node.args:
            return [Arg(value=self.default_length_value)]

        # If there's only an allowed chars kwarg, prepend the length arg.
        allowed_chars_kwarg = find_keyword_arg(node.args, "allowed_chars")

        if len(node.args) == 1 and allowed_chars_kwarg:
            return [
                Arg(value=self.default_length_value),
                allowed_chars_kwarg,
            ]

        # Otherwise don't do anything.
        return node.args
