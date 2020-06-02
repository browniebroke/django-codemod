from ..visitors.admin import InlineHasAddPermissionsTransformer
from ..visitors.encoding import ForceTextTransformer, SmartTextTransformer
from ..visitors.html import UnescapeEntitiesTransformer
from ..visitors.http import (
    HttpUrlQuotePlusTransformer,
    HttpUrlQuoteTransformer,
    HttpUrlUnQuotePlusTransformer,
    HttpUrlUnQuoteTransformer,
    IsSafeUrlTransformer,
)
from ..visitors.shortcuts import RenderToResponseTransformer
from ..visitors.translations import (
    UGetTextLazyTransformer,
    UGetTextNoopTransformer,
    UGetTextTransformer,
    UNGetTextLazyTransformer,
    UNGetTextTransformer,
)
from ..visitors.urls import URLTransformer
from .base import BaseCodemodCommand


class Django30Command(BaseCodemodCommand):
    """
    Resolve following deprecations:

    - Replaces ``render_to_response()`` by ``render()`` and add ``request=None``
      as the first argument of ``render()``.
    - Add the ``obj`` argument to ``InlineModelAdmin.has_add_permission()``.
    """

    DESCRIPTION: str = "Resolve deprecations for removals in Django 3.0."
    transformers = [
        RenderToResponseTransformer,
        InlineHasAddPermissionsTransformer,
    ]


class Django40Command(BaseCodemodCommand):
    """
    Resolve following deprecations:

    - ``django.utils.encoding.force_text``
    - ``django.utils.encoding.smart_text``
    - ``django.utils.http.urlquote``
    - ``django.utils.http.urlquote_plus``
    - ``django.utils.http.urlunquote``
    - ``django.utils.http.urlunquote_plus``
    - ``django.utils.http.is_safe_url``
    - ``django.utils.text.unescape_entities``
    - ``django.utils.translation.ugettext``
    - ``django.utils.translation.ugettext_lazy``
    - ``django.utils.translation.ugettext_noop``
    - ``django.utils.translation.ungettext``
    - ``django.utils.translation.ungettext_lazy``
    - ``django.conf.urls.url``
    """

    DESCRIPTION: str = "Resolve deprecations of things removed in Django 4.0"
    transformers = [
        ForceTextTransformer,
        HttpUrlQuotePlusTransformer,
        HttpUrlQuoteTransformer,
        HttpUrlUnQuotePlusTransformer,
        HttpUrlUnQuoteTransformer,
        IsSafeUrlTransformer,
        SmartTextTransformer,
        UGetTextLazyTransformer,
        UGetTextNoopTransformer,
        UGetTextTransformer,
        UNGetTextLazyTransformer,
        UNGetTextTransformer,
        URLTransformer,
        UnescapeEntitiesTransformer,
    ]
