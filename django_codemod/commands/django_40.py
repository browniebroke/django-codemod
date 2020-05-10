"""
Module to fix things removed in Django 4.0.

This is expected to cover most of the things listed in this section:
https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0
"""
from typing import Union

from libcst import (
    matchers as m,
    RemovalSentinel,
    Call,
    BaseExpression,
    Name,
    RemoveFromParent,
)
from libcst._nodes.statement import ImportFrom, BaseSmallStatement
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor

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


class URLToRePathCommand(VisitorBasedCodemodCommand):
    """Resolve deprecation of django.conf.urls.url."""

    def _test_import_from(self, node: ImportFrom) -> bool:
        return m.matches(
            node,
            m.ImportFrom(
                module=m.Attribute(
                    value=m.Attribute(
                        value=m.Name("django"), attr=m.Name(value="conf")
                    ),
                    attr=m.Name("urls"),
                ),
            ),
        )

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if self._test_import_from(updated_node):
            new_names = []
            new_import_missing = True
            new_import_alias = None
            for import_alias in original_node.names:
                if import_alias.evaluated_name == "url":
                    AddImportsVisitor.add_needed_import(
                        self.context, "django.urls", "re_path",
                    )
                else:
                    if import_alias.evaluated_name == "re_path":
                        new_import_missing = False
                    new_names.append(import_alias)
            if new_import_missing and new_import_alias is not None:
                new_names.append(new_import_alias)
            if not new_names:
                return RemoveFromParent()
            new_names = list(sorted(new_names, key=lambda n: n.evaluated_name))
            return ImportFrom(module=updated_node.module, names=new_names)
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if m.matches(updated_node, m.Call(func=m.Name("url"))):
            return Call(args=updated_node.args, func=Name("re_path"))
        return super().leave_Call(original_node, updated_node)
