from .base import BaseCodemodCommand
from ..visitors.django_30 import RenderToResponseToRenderTransformer
from ..visitors.django_40 import (
    ForceTextToForceStrTransformer,
    SmartTextToForceStrTransformer,
    UGetTextLazyToGetTextLazyTransformer,
    UGetTextNoopToGetTextNoopTransformer,
    UGetTextToGetTextTransformer,
    UNGetTextLazyToNGetTextLazyTransformer,
    UNGetTextToNGetTextTransformer,
    URLToRePathTransformer,
)


class Django30Command(BaseCodemodCommand):
    """
    Resolve deprecations for removals in Django 3.0.

    Combines all the other commands in this module, to fix these deprecations:

    - ``django.shortcuts.render_to_response``
    """

    DESCRIPTION: str = "Resolve deprecations for removals in Django 3.0."
    transformers = [
        RenderToResponseToRenderTransformer,
    ]


class Django40Command(BaseCodemodCommand):
    """
    Resolve deprecations for removals in Django 4.0.

    Combines all the other commands in this module, to fix these deprecations:

    - ``django.utils.encoding.force_text``
    - ``django.utils.encoding.smart_text``
    - ``django.utils.translation.ugettext``
    - ``django.utils.translation.ugettext_lazy``
    - ``django.utils.translation.ugettext_noop``
    - ``django.utils.translation.ungettext``
    - ``django.utils.translation.ungettext_lazy``
    - ``django.conf.urls.url``
    """

    DESCRIPTION: str = "Resolve deprecations of things removed in Django 4.0"
    transformers = [
        ForceTextToForceStrTransformer,
        SmartTextToForceStrTransformer,
        UGetTextLazyToGetTextLazyTransformer,
        UGetTextNoopToGetTextNoopTransformer,
        UGetTextToGetTextTransformer,
        UNGetTextLazyToNGetTextLazyTransformer,
        UNGetTextToNGetTextTransformer,
        URLToRePathTransformer,
    ]
