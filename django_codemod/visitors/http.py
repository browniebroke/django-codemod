from libcst import BaseExpression, Call
from libcst import matchers as m

from django_codemod.constants import DJANGO_2_0, DJANGO_2_1, DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import (
    BaseDjCodemodTransformer,
    BaseFuncRenameTransformer,
)


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


class HttpRequestXReadLinesTransformer(BaseDjCodemodTransformer):
    """Replace `HttpRequest.xreadlines()` by iterating over the request."""

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0

    # This should be conservative and only apply changes to:
    # - variables called `request`/`req`
    # - `request`/`req` attributes (e.g `self.request`/`view.req`...)
    matcher = m.Call(
        func=m.Attribute(
            value=m.OneOf(
                m.Name(value="request"),
                m.Name(value="req"),
                m.Attribute(attr=m.Name(value="request")),
                m.Attribute(attr=m.Name(value="req")),
            ),
            attr=m.Name(value="xreadlines"),
        )
    )

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if m.matches(updated_node, self.matcher):
            return updated_node.func.value
        return super().leave_Call(original_node, updated_node)


class CookieDateTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.http.cookie_date()` by `http_date`."""

    deprecated_in = DJANGO_2_1
    removed_in = DJANGO_3_0
    rename_from = "django.utils.http.cookie_date"
    rename_to = "django.utils.http.http_date"
