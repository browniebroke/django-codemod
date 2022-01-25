from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class UGetTextTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.translation.ugettext` by `gettext`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ugettext"
    rename_to = "django.utils.translation.gettext"


class UGetTextLazyTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.translation.ugettext_lazy` by `gettext_lazy`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ugettext_lazy"
    rename_to = "django.utils.translation.gettext_lazy"


class UGetTextNoopTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.translation.ugettext_noop` by `gettext_noop`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ugettext_noop"
    rename_to = "django.utils.translation.gettext_noop"


class UNGetTextTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.translation.ungettext` by `ngettext`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ungettext"
    rename_to = "django.utils.translation.ngettext"


class UNGetTextLazyTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils.translation.ungettext_lazy` by `ngettext_lazy`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.utils.translation.ungettext_lazy"
    rename_to = "django.utils.translation.ngettext_lazy"
