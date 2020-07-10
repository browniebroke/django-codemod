from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class UGetTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ugettext"
    rename_to = "django.utils.translation.gettext"


class UGetTextLazyTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext_lazy``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ugettext_lazy"
    rename_to = "django.utils.translation.gettext_lazy"


class UGetTextNoopTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ugettext_noop``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ugettext_noop"
    rename_to = "django.utils.translation.gettext_noop"


class UNGetTextTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ungettext``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ungettext"
    rename_to = "django.utils.translation.ngettext"


class UNGetTextLazyTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.translation.ungettext_lazy``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ungettext_lazy"
    rename_to = "django.utils.translation.ngettext_lazy"
