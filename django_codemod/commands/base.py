"""Module to implement base functionality."""

from abc import ABC
from typing import Union

from libcst import matchers as m, RemovalSentinel, Call, BaseExpression, Name
from libcst._nodes.statement import ImportFrom, BaseSmallStatement, ImportAlias
from libcst.codemod import VisitorBasedCodemodCommand


class BaseSimpleFuncRename(VisitorBasedCodemodCommand, ABC):
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
