"""Module to implement base functionality."""
from abc import ABC
from typing import Generator, Optional, Sequence, Tuple, Union

from libcst import (
    Arg,
    BaseExpression,
    BaseSmallStatement,
    Call,
    CSTNode,
    ImportAlias,
    ImportFrom,
    ImportStar,
    MaybeSentinel,
    Name,
    RemovalSentinel,
    RemoveFromParent,
)
from libcst import matchers as m
from libcst.codemod import ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor
from libcst.metadata import Scope, ScopeProvider


class BaseDjCodemodTransformer(ContextAwareTransformer, ABC):
    deprecated_in: Tuple[int, int]
    removed_in: Tuple[int, int]


def module_matcher(import_parts: Sequence) -> Union[m.BaseMatcherNode, m.DoNotCare]:
    """Build matcher for a module given sequence of import parts."""
    # If only one element, it is just a Name
    if len(import_parts) == 1:
        return m.Name(import_parts[0])
    *values, attr = import_parts
    value = module_matcher(values)
    return m.Attribute(value=value, attr=m.Name(attr))


def import_from_matches(node: ImportFrom, module_parts: Sequence) -> bool:
    """Check if an `ImportFrom` node matches sequence of module parts."""
    return m.matches(node, m.ImportFrom(module=module_matcher(module_parts)))


class BaseRenameTransformer(BaseDjCodemodTransformer, ABC):
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
        self.save_import_scope(original_node)
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
                if self.rename_from != self.rename_to:
                    if self.simple_rename:
                        self.add_new_import(import_alias.evaluated_name)
                    continue
            yield import_alias

    def resolve_scope(self, node: CSTNode) -> Scope:
        scopes_map = self.context.wrapper.resolve(ScopeProvider)
        return scopes_map[node]

    def save_import_scope(self, import_from: ImportFrom) -> None:
        scope = self.resolve_scope(import_from)
        self.context.scratch[self.ctx_key_import_scope] = scope

    @property
    def import_scope(self) -> Optional[Scope]:
        return self.context.scratch.get(self.ctx_key_import_scope, None)

    @property
    def ctx_key_import_scope(self) -> str:
        return f"{self.rename_from}-import_scope"

    @staticmethod
    def tidy_new_imported_names(
        new_names: Sequence[ImportAlias],
    ) -> Sequence[ImportAlias]:
        """Tidy up the updated list of imports"""
        # Sort them
        cleaned_names = sorted(new_names, key=lambda n: n.evaluated_name)
        # Remove any trailing commas
        last_name = cleaned_names[-1]
        if last_name.comma != MaybeSentinel.DEFAULT:
            cleaned_names[-1] = last_name.with_changes(comma=MaybeSentinel.DEFAULT)
        return cleaned_names

    def add_new_import(self, evaluated_name: Optional[str] = None) -> None:
        as_name = (
            self.entity_imported_as.name.value if self.entity_imported_as else None
        )
        AddImportsVisitor.add_needed_import(
            context=self.context,
            module=".".join(self.new_module_parts),
            obj=self.new_name or evaluated_name,
            asname=as_name,
        )

    @property
    def ctx_key_is_name_called(self):
        return f"{self.rename_from}-is_name_called"

    @property
    def entity_is_name_called(self):
        return self.context.scratch.get(self.ctx_key_is_name_called, False)

    def visit_Call(self, node: Call) -> Optional[bool]:
        if self.is_imported_with_old_name and m.matches(
            node, m.Call(func=m.Name(self.old_name))
        ):
            self.context.scratch[self.ctx_key_is_name_called] = True
        return None

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        self.context.scratch.pop(self.ctx_key_is_name_called, None)
        return super().leave_Call(original_node, updated_node)

    def leave_Name(self, original_node: Name, updated_node: Name) -> BaseExpression:
        if (
            self.is_imported_with_old_name
            and not self.entity_is_name_called
            and m.matches(updated_node, m.Name(value=self.old_name))
        ):
            try:
                scope = self.resolve_scope(original_node)
            except KeyError:
                # Can't resolve scope of original_node, ignore it
                # Might be because of one of these reasons:
                # - It's the same name in another scope
                # - It's a attribute with the same name
                # - It's a keyword argument
                pass
            else:
                if scope == self.import_scope:
                    return updated_node.with_changes(value=self.new_name)
        return super().leave_Name(original_node, updated_node)


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
