from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class URLTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.conf.urls.url``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"
