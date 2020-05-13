# This is expected to cover most of the things listed in this section:
# https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0
from .base import BaseSimpleFuncRenameTransformer


class ForceTextToForceStrTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.force_text``."""

    rename_from = "django.utils.encoding.force_text"
    rename_to = "django.utils.encoding.force_str"


class SmartTextToForceStrTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.encoding.smart_text``."""

    rename_from = "django.utils.encoding.smart_text"
    rename_to = "django.utils.encoding.smart_str"


class UGetTextToGetTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext``."""

    rename_from = "django.utils.translation.ugettext"
    rename_to = "django.utils.translation.gettext"


class UGetTextLazyToGetTextLazyTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext_lazy``."""

    rename_from = "django.utils.translation.ugettext_lazy"
    rename_to = "django.utils.translation.gettext_lazy"


class UGetTextNoopToGetTextNoopTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext_noop``."""

    rename_from = "django.utils.translation.ugettext_noop"
    rename_to = "django.utils.translation.gettext_noop"


class UNGetTextToNGetTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ungettext``."""

    rename_from = "django.utils.translation.ungettext"
    rename_to = "django.utils.translation.ngettext"


class UNGetTextLazyToNGetTextLazyTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ungettext_lazy``."""

    rename_from = "django.utils.translation.ungettext_lazy"
    rename_to = "django.utils.translation.ngettext_lazy"


class URLToRePathTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.conf.urls.url``."""

    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"
