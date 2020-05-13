# This is expected to cover most of the things listed in this section:
# https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0
from .base import BaseCodemodCommand
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


class ForceTextToForceStrCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.encoding.force_text``."""

    DESCRIPTION: str = "Replaces force_text() by force_str()."
    transformers = [ForceTextToForceStrTransformer]


class SmartTextToForceStrCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.encoding.smart_text``."""

    DESCRIPTION: str = "Replaces smart_text() by smart_str()."
    transformers = [SmartTextToForceStrTransformer]


class UGetTextToGetTextCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.translation.ugettext``."""

    DESCRIPTION: str = "Replaces ugettext() by gettext()."
    transformers = [UGetTextToGetTextTransformer]


class UGetTextLazyToGetTextLazyCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.translation.ugettext_lazy``."""

    DESCRIPTION: str = "Replaces ugettext_lazy() by gettext_lazy()."
    transformers = [UGetTextLazyToGetTextLazyTransformer]


class UGetTextNoopToGetTextNoopCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.translation.ugettext_noop``."""

    DESCRIPTION: str = "Replaces ugettext_noop() by gettext_noop()."
    transformers = [UGetTextNoopToGetTextNoopTransformer]


class UNGetTextToNGetTextCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.translation.ungettext``."""

    DESCRIPTION: str = "Replaces ungettext() by ngettext()."
    transformers = [UNGetTextToNGetTextTransformer]


class UNGetTextLazyToNGetTextLazyCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.utils.translation.ungettext_lazy``."""

    DESCRIPTION: str = "Replaces ungettext_lazy() by ngettext_lazy()."
    transformers = [UNGetTextLazyToNGetTextLazyTransformer]


class URLToRePathCommand(BaseCodemodCommand):
    """Resolve deprecation of ``django.conf.urls.url``."""

    DESCRIPTION: str = "Replaces url() by re_path()."
    transformers = [URLToRePathTransformer]
