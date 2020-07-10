from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class UnescapeEntitiesTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.text.unescape_entities``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.text.unescape_entities"
    rename_to = "html.unescape"
