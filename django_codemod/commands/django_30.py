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
