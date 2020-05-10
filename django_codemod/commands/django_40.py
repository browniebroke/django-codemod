"""Module to update CDjango 4.0 deprecations."""
from abc import ABC
from typing import Union

from libcst import matchers as m, RemovalSentinel, Call, BaseExpression, Name
from libcst._nodes.statement import ImportFrom, BaseSmallStatement, ImportAlias
from libcst.codemod import VisitorBasedCodemodCommand


class BaseFuncRename(VisitorBasedCodemodCommand, ABC):
    """Base class to help rename a simple function."""

    old_name: str
    new_name: str

    def _test_import_from(self, node: ImportFrom) -> bool:
        """Check if 'import from' should be updated."""
        raise NotImplementedError()

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if self._test_import_from(updated_node):
            new_names = []
            new_import_missing = True
            new_import_alias = None
            for import_alias in original_node.names:
                if import_alias.evaluated_name == self.old_name:
                    new_import_alias = ImportAlias(name=Name(self.new_name))
                else:
                    if import_alias.evaluated_name == self.new_name:
                        new_import_missing = False
                    new_names.append(import_alias)
            if new_import_missing and new_import_alias is not None:
                new_names.append(new_import_alias)
            new_names = list(sorted(new_names, key=lambda n: n.evaluated_name))
            return ImportFrom(module=updated_node.module, names=new_names)
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if m.matches(updated_node, m.Call(func=m.Name(self.old_name))):
            return Call(args=updated_node.args, func=Name(self.new_name))
        return super().leave_Call(original_node, updated_node)


class ForceTextToForceStrCommand(BaseFuncRename):
    """Help resolve deprecation of django.utils.encoding.force_text."""

    DESCRIPTION: str = "Replaces force_text() by force_str()."
    old_name = "force_text"
    new_name = "force_str"

    def _test_import_from(self, node: ImportFrom) -> bool:
        return m.matches(
            node,
            m.ImportFrom(
                module=m.Attribute(
                    attr=m.Name("encoding"),
                    value=m.Attribute(
                        value=m.Name("django"), attr=m.Name(value="utils")
                    ),
                ),
            ),
        )


class SmartTextToForceStrCommand(ForceTextToForceStrCommand):
    """Help resolve deprecation of django.utils.encoding.smart_text."""

    DESCRIPTION: str = "Replaces smart_text() by smart_str()."
    old_name = "smart_text"
    new_name = "smart_str"


class UGetTextToGetTextCommand(BaseFuncRename):
    """Help resolve deprecation of django.utils.translation.ugettext."""

    DESCRIPTION: str = "Replaces ugettext() by gettext()."
    old_name = "ugettext"
    new_name = "gettext"

    def _test_import_from(self, node: ImportFrom) -> bool:
        return m.matches(
            node,
            m.ImportFrom(
                module=m.Attribute(
                    attr=m.Name("translation"),
                    value=m.Attribute(
                        value=m.Name("django"), attr=m.Name(value="utils")
                    ),
                ),
            ),
        )
