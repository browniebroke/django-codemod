from django_codemod.constants import DJANGO_2_0, DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class ForceTextTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.force_text``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.encoding.force_text"
    rename_to = "django.utils.encoding.force_str"


class SmartTextTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.smart_text``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.encoding.smart_text"
    rename_to = "django.utils.encoding.smart_str"


class UnicodeCompatibleTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.python_2_unicode_compatible``."""

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0
    rename_from = "django.utils.encoding.python_2_unicode_compatible"
    rename_to = "six.python_2_unicode_compatible"
