from django_codemod.constants import DJANGO_1_10, DJANGO_2_0
from django_codemod.visitors.base import BaseModuleRenameTransformer


class URLResolversTransformer(BaseModuleRenameTransformer):
    """Resolve deprecation of ``django.core.urlresolvers``."""

    deprecated_in = DJANGO_1_10
    removed_in = DJANGO_2_0
    rename_from = "django.core.urlresolvers"
    rename_to = "django.urls"
