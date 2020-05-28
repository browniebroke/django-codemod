from django_codemod.constants import DJANGO_20, DJANGO_40
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class URLToRePathTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.conf.urls.url``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_40
    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"
