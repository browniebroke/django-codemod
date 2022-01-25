from django_codemod.constants import DJANGO_2_0, DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class ForceTextTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.encoding.force_text` by `force_str`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.encoding.force_text"
    rename_to = "django.utils.encoding.force_str"


class SmartTextTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.encoding.smart_text` by `smart_str`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.encoding.smart_text"
    rename_to = "django.utils.encoding.smart_str"


class UnicodeCompatibleTransformer(BaseFuncRenameTransformer):
    """Replace Django's `python_2_unicode_compatible` by the one from `six`."""

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0
    rename_from = "django.utils.encoding.python_2_unicode_compatible"
    rename_to = "six.python_2_unicode_compatible"
