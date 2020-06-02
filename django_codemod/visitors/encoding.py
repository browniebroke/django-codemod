from django_codemod.constants import DJANGO_30, DJANGO_40
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class ForceTextToForceStrTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.force_text``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.encoding.force_text"
    rename_to = "django.utils.encoding.force_str"


class SmartTextToForceStrTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.smart_text``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.encoding.smart_text"
    rename_to = "django.utils.encoding.smart_str"
