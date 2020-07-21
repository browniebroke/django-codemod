from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class HttpUrlQuoteTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlquote``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlquote"
    rename_to = "urllib.parse.quote"


class HttpUrlQuotePlusTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlquote_plus``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlquote_plus"
    rename_to = "urllib.parse.quote_plus"


class HttpUrlUnQuoteTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlunquote``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlunquote"
    rename_to = "urllib.parse.unquote"


class HttpUrlUnQuotePlusTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.urlunquote_plus``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlunquote_plus"
    rename_to = "urllib.parse.unquote_plus"


class IsSafeUrlTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.http.is_safe_url``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.is_safe_url"
    rename_to = "django.utils.http.url_has_allowed_host_and_scheme"
