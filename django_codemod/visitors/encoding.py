from django_codemod.constants import DJANGO_20, DJANGO_30, DJANGO_40
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class ForceTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.force_text``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.encoding.force_text"
    rename_to = "django.utils.encoding.force_str"


class SmartTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.smart_text``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.encoding.smart_text"
    rename_to = "django.utils.encoding.smart_str"


class UnicodeCompatibleTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.python_2_unicode_compatible``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_30
    rename_from = "django.utils.encoding.python_2_unicode_compatible"
    rename_to = "six.python_2_unicode_compatible"
