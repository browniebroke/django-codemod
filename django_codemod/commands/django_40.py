"""
Module to fix things removed in Django 4.0.

This is expected to cover most of the things listed in this section:
https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0
"""
from django_codemod.commands.base import BaseSimpleFuncRename


class ForceTextToForceStrCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.encoding.force_text."""

    DESCRIPTION: str = "Replaces force_text() by force_str()."
    rename_from = "django.utils.encoding.force_text"
    rename_to = "django.utils.encoding.force_str"


class SmartTextToForceStrCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.encoding.smart_text."""

    DESCRIPTION: str = "Replaces smart_text() by smart_str()."
    rename_from = "django.utils.encoding.smart_text"
    rename_to = "django.utils.encoding.smart_str"


class UGetTextToGetTextCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.translation.ugettext."""

    DESCRIPTION: str = "Replaces ugettext() by gettext()."
    rename_from = "django.utils.translation.ugettext"
    rename_to = "django.utils.translation.gettext"


class UGetTextLazyToGetTextLazyCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.translation.ugettext_lazy."""

    DESCRIPTION: str = "Replaces ugettext_lazy() by gettext_lazy()."
    rename_from = "django.utils.translation.ugettext_lazy"
    rename_to = "django.utils.translation.gettext_lazy"


class UGetTextNoopToGetTextNoopCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.translation.ugettext_noop."""

    DESCRIPTION: str = "Replaces ugettext_noop() by gettext_noop()."
    rename_from = "django.utils.translation.ugettext_noop"
    rename_to = "django.utils.translation.gettext_noop"


class UNGetTextToNGetTextCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.translation.ungettext."""

    DESCRIPTION: str = "Replaces ungettext() by ngettext()."
    rename_from = "django.utils.translation.ungettext"
    rename_to = "django.utils.translation.ngettext"


class UNGetTextLazyToNGetTextLazyCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.translation.ungettext_lazy."""

    DESCRIPTION: str = "Replaces ungettext_lazy() by ngettext_lazy()."
    rename_from = "django.utils.translation.ungettext_lazy"
    rename_to = "django.utils.translation.ngettext_lazy"


class URLToRePathCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.conf.urls.url."""

    DESCRIPTION: str = "Replaces url() by re_path()."
    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"
