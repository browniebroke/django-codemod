from django_codemod.constants import DJANGO_20, DJANGO_40
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class UGetTextToGetTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_40
    rename_from = "django.utils.translation.ugettext"
    rename_to = "django.utils.translation.gettext"


class UGetTextLazyToGetTextLazyTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext_lazy``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_40
    rename_from = "django.utils.translation.ugettext_lazy"
    rename_to = "django.utils.translation.gettext_lazy"


class UGetTextNoopToGetTextNoopTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext_noop``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_40
    rename_from = "django.utils.translation.ugettext_noop"
    rename_to = "django.utils.translation.gettext_noop"


class UNGetTextToNGetTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ungettext``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_40
    rename_from = "django.utils.translation.ungettext"
    rename_to = "django.utils.translation.ngettext"


class UNGetTextLazyToNGetTextLazyTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ungettext_lazy``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_40
    rename_from = "django.utils.translation.ungettext_lazy"
    rename_to = "django.utils.translation.ngettext_lazy"
