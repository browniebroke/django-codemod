from libcst import BaseExpression, Call, Name
from libcst import matchers as m

from django_codemod.constants import DJANGO_2_0, DJANGO_3_0
from django_codemod.visitors.base import BaseRenameTransformer


class ContextDecoratorTransformer(BaseRenameTransformer):
    """Replace Django's `ContextDecorator` decorator by the `contextlib`'s one."""

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0
    rename_from = "django.utils.decorators.ContextDecorator"
    rename_to = "contextlib.ContextDecorator"


class AvailableAttrsTransformer(BaseRenameTransformer):
    """Replace `django.utils.decorators.available_attrs` by `WRAPPER_ASSIGNMENTS`."""

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0
    rename_from = "django.utils.decorators.available_attrs"
    rename_to = "functools.WRAPPER_ASSIGNMENTS"

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        matcher = self.name_matcher
        if m.matches(updated_node, m.Call(func=matcher)):
            return Name(self.new_name)
        return super().leave_Call(original_node, updated_node)
