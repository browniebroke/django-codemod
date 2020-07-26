from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class HttpUrlQuoteTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.http.urlquote` by `urllib.parse.quote`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlquote"
    rename_to = "urllib.parse.quote"


class HttpUrlQuotePlusTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.http.urlquote_plus` by `urllib.parse.quote_plus`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlquote_plus"
    rename_to = "urllib.parse.quote_plus"


class HttpUrlUnQuoteTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.http.urlunquote` by `urllib.parse.unquote`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlunquote"
    rename_to = "urllib.parse.unquote"


class HttpUrlUnQuotePlusTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.http.urlunquote_plus` by `urllib.parse.unquote_plus`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.urlunquote_plus"
    rename_to = "urllib.parse.unquote_plus"


class IsSafeUrlTransformer(BaseFuncRenameTransformer):
    """Rename `django.utils.http.is_safe_url` to `url_has_allowed_host_and_scheme`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.http.is_safe_url"
    rename_to = "django.utils.http.url_has_allowed_host_and_scheme"
