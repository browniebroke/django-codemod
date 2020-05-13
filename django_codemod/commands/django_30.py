# This is expected to cover most of the things listed in this section:
# https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-0
from .base import BaseCodemodCommand
from ..visitors.django_30 import RenderToResponseToRenderTransformer


class RenderToResponseToRenderCommand(BaseCodemodCommand):
    """
    Resolve deprecation of ``django.shortcuts.render_to_response``.

    Replaces ``render_to_response()`` by ``render()`` and add
    ``request=None`` as the first argument of ``render()``.
    """

    DESCRIPTION: str = "Replaces render_to_response() by render()."
    transformers = [RenderToResponseToRenderTransformer]


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
