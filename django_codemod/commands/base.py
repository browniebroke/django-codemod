"""Module to implement base functionality."""

from abc import ABC
from typing import Union, Sequence

from libcst import (
    matchers as m,
    RemovalSentinel,
    Call,
    BaseExpression,
    Name,
    RemoveFromParent,
    Arg,
)
from libcst._nodes.statement import ImportFrom, BaseSmallStatement
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor


def module_matcher(import_parts):
    *values, attr = import_parts
    if len(values) > 1:
        value = module_matcher(values)
    elif len(values) == 1:
        value = m.Name(values[0])
    else:
        value = None
    return m.Attribute(value=value, attr=m.Name(attr))


class BaseSimpleFuncRename(VisitorBasedCodemodCommand, ABC):
    """Base class to help rename a simple function."""

    rename_from: str
    rename_to: str

    @property
    def old_name(self):
        return self.rename_from.split(".")[-1]

    @property
    def old_module_parts(self):
        return self.rename_from.split(".")[:-1]

    @property
    def new_name(self):
        return self.rename_to.split(".")[-1]

    @property
    def new_module_parts(self):
        return self.rename_to.split(".")[:-1]

    def _test_import_from(self, node: ImportFrom) -> bool:
        """Check if 'import from' should be updated."""
        return m.matches(
            node, m.ImportFrom(module=module_matcher(self.old_module_parts))
        )

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if self._test_import_from(updated_node):
            new_names = []
            for import_alias in original_node.names:
                if import_alias.evaluated_name == self.old_name:
                    AddImportsVisitor.add_needed_import(
                        self.context, ".".join(self.new_module_parts), self.new_name,
                    )
                else:
                    new_names.append(import_alias)
            if not new_names:
                return RemoveFromParent()
            new_names = list(sorted(new_names, key=lambda n: n.evaluated_name))
            return ImportFrom(module=updated_node.module, names=new_names)
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if m.matches(updated_node, m.Call(func=m.Name(self.old_name))):
            updated_args = self.update_call_args(updated_node)
            return Call(args=updated_args, func=Name(self.new_name))
        return super().leave_Call(original_node, updated_node)

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return node.args
