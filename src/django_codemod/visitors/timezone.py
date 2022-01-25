from typing import Sequence

from libcst import Arg, Call, Integer, parse_expression
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import DJANGO_2_2, DJANGO_3_1
from django_codemod.visitors.base import BaseFuncRenameTransformer


class FixedOffsetTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.timezone.FixedOffset` by `datetime.timezone`."""

    deprecated_in = DJANGO_2_2
    removed_in = DJANGO_3_1
    rename_from = "django.utils.timezone.FixedOffset"
    rename_to = "datetime.timezone"

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        """Update first argument to convert integer for minutes to timedelta."""
        AddImportsVisitor.add_needed_import(
            context=self.context,
            module="datetime",
            obj="timedelta",
        )
        offset_arg, *other_args = node.args
        integer_value = offset_arg.value
        if not isinstance(integer_value, Integer):
            raise AssertionError(f"Unexpected type for: {integer_value}")
        timedelta_call = parse_expression(f"timedelta(minutes={integer_value.value})")
        new_offset_arg = offset_arg.with_changes(value=timedelta_call)
        return (new_offset_arg, *other_args)
