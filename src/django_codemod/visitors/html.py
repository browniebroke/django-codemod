from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class UnescapeEntitiesTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.text.unescape_entities` by `html.unescape`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.text.unescape_entities"
    rename_to = "html.unescape"
