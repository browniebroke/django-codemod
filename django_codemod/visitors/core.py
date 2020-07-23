from django_codemod.constants import DJANGO_1_10, DJANGO_2_0
from django_codemod.visitors.base import BaseModuleRenameTransformer


class URLResolversTransformer(BaseModuleRenameTransformer):
    """Replace `django.core.urlresolvers` by `django.urls`."""

    deprecated_in = DJANGO_1_10
    removed_in = DJANGO_2_0
    rename_from = "django.core.urlresolvers"
    rename_to = "django.urls"
