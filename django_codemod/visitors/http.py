from django_codemod.constants import DJANGO_30, DJANGO_40
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class HttpUrlQuoteTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlquote``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.http.urlquote"
    rename_to = "urllib.parse.quote"


class HttpUrlQuotePlusTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlquote_plus``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.http.urlquote_plus"
    rename_to = "urllib.parse.quote_plus"


class HttpUrlUnQuoteTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlunquote``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.http.urlunquote"
    rename_to = "urllib.parse.unquote"


class HttpUrlUnQuotePlusTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlunquote_plus``."""

    deprecated_in = DJANGO_30
    removed_in = DJANGO_40
    rename_from = "django.utils.http.urlunquote_plus"
    rename_to = "urllib.parse.unquote_plus"
