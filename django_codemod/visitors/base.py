"""Module to implement base functionality."""
from abc import ABC
from typing import Generator, Optional, Sequence, Union

from libcst import (
    Arg,
    BaseExpression,
    Call,
    ImportStar,
    MaybeSentinel,
    Name,
    RemovalSentinel,
    RemoveFromParent,
)
from libcst import matchers as m
from libcst._nodes.statement import BaseSmallStatement, ImportAlias, ImportFrom
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


def import_from_matches(node, module_parts):
    return m.matches(node, m.ImportFrom(module=module_matcher(module_parts)))


class BaseRenameTransformer(ContextAwareTransformer, ABC):
    """Base class to help rename or move a declaration."""

    rename_from: str
    rename_to: str

    simple_rename = True

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
    def ctx_key_imported_as(self):
        return f"{self.rename_from}-imported_as"

    @property
    def entity_imported_as(self):
        return self.context.scratch.get(self.ctx_key_imported_as, None)

    @property
    def is_imported_with_old_name(self):
        is_imported = self.ctx_key_imported_as in self.context.scratch
        return is_imported and not self.entity_imported_as

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        """Update import statements for matching old module name."""
        if not import_from_matches(updated_node, self.old_module_parts):
            return super().leave_ImportFrom(original_node, updated_node)
        # This is a match
        new_names = list(self.gen_new_imported_names(updated_node.names))
        if not new_names:
            # Nothing left in the import statement: remove it
            return RemoveFromParent()
        # Some imports are left, update the statement
        cleaned_names = self.tidy_new_imported_names(new_names)
        return updated_node.with_changes(names=cleaned_names)

    def gen_new_imported_names(
        self, old_names: Union[Sequence[ImportAlias], ImportStar]
    ) -> Generator:
        """Update import if the entity we're interested in is imported."""
        for import_alias in old_names:
            if not self.old_name or import_alias.evaluated_name == self.old_name:
                self.context.scratch[self.ctx_key_imported_as] = import_alias.asname
                if self.simple_rename:
                    self.add_new_import(import_alias.evaluated_name)
            else:
                yield import_alias

    def tidy_new_imported_names(self, new_names):
        """Tidy up the updated list of imports"""
        # Sort them
        cleaned_names = sorted(new_names, key=lambda n: n.evaluated_name)
        # Remove any trailing commas
        last_name = cleaned_names[-1]
        if last_name.comma != MaybeSentinel.DEFAULT:
            cleaned_names[-1] = last_name.with_changes(comma=MaybeSentinel.DEFAULT)
        return cleaned_names

    def add_new_import(self, evaluated_name: Optional[str] = None):
        as_name = (
            self.entity_imported_as.name.value if self.entity_imported_as else None
        )
        AddImportsVisitor.add_needed_import(
            context=self.context,
            module=".".join(self.new_module_parts),
            obj=self.new_name or evaluated_name,
            asname=as_name,
        )


class BaseModuleRenameTransformer(BaseRenameTransformer, ABC):
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


class BaseFuncRenameTransformer(BaseRenameTransformer, ABC):
    """Base class to help rename or move a function."""

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if self.is_imported_with_old_name and m.matches(
            updated_node, m.Call(func=m.Name(self.old_name))
        ):
            return self.update_call(updated_node=updated_node)
        return super().leave_Call(original_node, updated_node)

    def update_call(self, updated_node: Call) -> BaseExpression:
        updated_args = self.update_call_args(updated_node)
        return Call(args=updated_args, func=Name(self.new_name))

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return node.args
