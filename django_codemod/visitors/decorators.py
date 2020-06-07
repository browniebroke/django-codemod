from django_codemod.constants import DJANGO_20, DJANGO_30
from django_codemod.visitors.base import BaseSimpleRenameTransformer


class ContextDecoratorTransformer(BaseSimpleRenameTransformer):
    """Resolve deprecation of ``django.utils.decorators.ContextDecorator``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_30
    rename_from = "django.utils.decorators.ContextDecorator"
    rename_to = "contextlib.ContextDecorator"
