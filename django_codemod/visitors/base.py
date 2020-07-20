"""Module to implement base functionality."""
from abc import ABC
from typing import Sequence, Union

from libcst import (
    Arg,
    BaseExpression,
    Call,
    MaybeSentinel,
    Name,
    RemovalSentinel,
    RemoveFromParent,
)
from libcst import matchers as m
from libcst._nodes.statement import BaseSmallStatement, ImportFrom
from libcst.codemod import ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor


def module_matcher(import_parts):
    *values, attr = import_parts
    if len(values) > 1:
        value = module_matcher(values)
    elif len(values) == 1:
        value = m.Name(values[0])
    else:
        value = m.DoNotCare()
    return m.Attribute(value=value, attr=m.Name(attr))


class BaseSimpleRenameTransformer(ContextAwareTransformer, ABC):
    """Base class to help rename or move a declaration."""

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

    @property
    def ctx_key_is_imported(self):
        return f"{self.rename_from}-is_imported"

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if not m.matches(
            updated_node, m.ImportFrom(module=module_matcher(self.old_module_parts))
        ):
            return super().leave_ImportFrom(original_node, updated_node)
        new_names = []
        for import_alias in updated_node.names:
            if not self.old_name or import_alias.evaluated_name == self.old_name:
                as_name = (
                    import_alias.asname.name.value if import_alias.asname else None
                )
                self.add_new_import(
                    self.new_name or import_alias.evaluated_name, as_name
                )
                self.context.scratch[self.ctx_key_is_imported] = not import_alias.asname
            else:
                new_names.append(import_alias)
        if not new_names:
            return RemoveFromParent()
        # sort imports
        new_names = sorted(new_names, key=lambda n: n.evaluated_name)
        # remove any trailing commas
        last_name = new_names[-1]
        if last_name.comma != MaybeSentinel.DEFAULT:
            new_names[-1] = last_name.with_changes(comma=MaybeSentinel.DEFAULT)
        return updated_node.with_changes(names=new_names)

    @property
    def is_entity_imported(self):
        return self.context.scratch.get(self.ctx_key_is_imported, False)

    def add_new_import(self, new_name, as_name):
        AddImportsVisitor.add_needed_import(
            context=self.context,
            module=".".join(self.new_module_parts),
            obj=new_name,
            asname=as_name,
        )


class BaseSimpleModuleRenameTransformer(BaseSimpleRenameTransformer, ABC):
    """Base class to help rename or move a module."""

    @property
    def old_name(self):
        return ""

    @property
    def old_module_parts(self):
        return self.rename_from.split(".")

    @property
    def new_name(self):
        return ""

    @property
    def new_module_parts(self):
        return self.rename_to.split(".")


class BaseSimpleFuncRenameTransformer(BaseSimpleRenameTransformer, ABC):
    """Base class to help rename or move a function."""

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if self.is_entity_imported and m.matches(
            updated_node, m.Call(func=m.Name(self.old_name))
        ):
            return self.update_call(updated_node=updated_node)
        return super().leave_Call(original_node, updated_node)

    def update_call(self, updated_node: Call) -> BaseExpression:
        updated_args = self.update_call_args(updated_node)
        return Call(args=updated_args, func=Name(self.new_name))

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return node.args
