"""
Module to fix things removed in Django 4.0.

This is expected to cover most of the things listed in this section:
https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0
"""
from libcst import matchers as m
from libcst._nodes.statement import ImportFrom

from django_codemod.commands.base import BaseSimpleFuncRename


class ForceTextToForceStrCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.encoding.force_text."""

    DESCRIPTION: str = "Replaces force_text() by force_str()."
    old_name = "force_text"
    new_name = "force_str"

    def _test_import_from(self, node: ImportFrom) -> bool:
        return m.matches(
            node,
            m.ImportFrom(
                module=m.Attribute(
                    value=m.Attribute(
                        value=m.Name("django"), attr=m.Name(value="utils")
                    ),
                    attr=m.Name("encoding"),
                ),
            ),
        )


class SmartTextToForceStrCommand(ForceTextToForceStrCommand):
    """Resolve deprecation of django.utils.encoding.smart_text."""

    DESCRIPTION: str = "Replaces smart_text() by smart_str()."
    old_name = "smart_text"
    new_name = "smart_str"


class UGetTextToGetTextCommand(BaseSimpleFuncRename):
    """Resolve deprecation of django.utils.translation.ugettext."""

    DESCRIPTION: str = "Replaces ugettext() by gettext()."
    old_name = "ugettext"
    new_name = "gettext"

    def _test_import_from(self, node: ImportFrom) -> bool:
        return m.matches(
            node,
            m.ImportFrom(
                module=m.Attribute(
                    value=m.Attribute(
                        value=m.Name("django"), attr=m.Name(value="utils")
                    ),
                    attr=m.Name("translation"),
                ),
            ),
        )


class UGetTextLazyToGetTextLazyCommand(UGetTextToGetTextCommand):
    """Resolve deprecation of django.utils.translation.ugettext_lazy."""

    DESCRIPTION: str = "Replaces ugettext_lazy() by gettext_lazy()."
    old_name = "ugettext_lazy"
    new_name = "gettext_lazy"


class UGetTextNoopToGetTextNoopCommand(UGetTextToGetTextCommand):
    """Resolve deprecation of django.utils.translation.ugettext_noop."""

    DESCRIPTION: str = "Replaces ugettext_noop() by gettext_noop()."
    old_name = "ugettext_noop"
    new_name = "gettext_noop"


class UNGetTextToNGetTextCommand(UGetTextToGetTextCommand):
    """Resolve deprecation of django.utils.translation.ungettext."""

    DESCRIPTION: str = "Replaces ungettext() by ngettext()."
    old_name = "ungettext"
    new_name = "ngettext"


class UNGetTextLazyToNGetTextLazyCommand(UGetTextToGetTextCommand):
    """Resolve deprecation of django.utils.translation.ungettext_lazy."""

    DESCRIPTION: str = "Replaces ungettext_lazy() by ngettext_lazy()."
    old_name = "ungettext_lazy"
    new_name = "ngettext_lazy"
