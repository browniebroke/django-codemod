from django_codemod.constants import DJANGO_30, DJANGO_40
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class UnescapeEntitiesTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.text.unescape_entities``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.text.unescape_entities"
    rename_to = "html.unescape"
