"""Module to implement base functionality."""
from abc import ABC
from typing import List, Optional, Sequence, Tuple, Union

from libcst import (
    Arg,
    Attribute,
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
from libcst.codemod import CodemodContext, ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor
from libcst.metadata import ParentNodeProvider, Scope, ScopeProvider


class BaseDjCodemodTransformer(ContextAwareTransformer, ABC):
    deprecated_in: Tuple[int, int]
    removed_in: Tuple[int, int]


def module_matcher(
    import_parts: Sequence[str],
) -> Union[m.Attribute, m.Name]:
    """Build matcher for a module given sequence of import parts."""
    # If only one element, it is just a Name
    if len(import_parts) == 1:
        return m.Name(import_parts[0])
    *values, attr = import_parts
    value = module_matcher(values)
    return m.Attribute(value=value, attr=m.Name(attr))


def import_from_matches(node: ImportFrom, module_parts: Sequence[str]) -> bool:
    """Check if an `ImportFrom` node matches sequence of module parts."""
    return m.matches(node, m.ImportFrom(module=module_matcher(module_parts)))


class BaseRenameTransformer(BaseDjCodemodTransformer, ABC):
    """Base class to help rename or move a declaration."""

    rename_from: str
    rename_to: str

    simple_rename = True

    def __init__(self, context: CodemodContext) -> None:
        super().__init__(context)
        *self.old_parent_module_parts, self.old_parent_name, _ = (
            *self.old_module_parts,
            self.old_name,
        ) = self.old_all_parts = self.rename_from.split(".")
        *self.new_parent_module_parts, self.new_parent_name, _ = (
            *self.new_module_parts,
            self.new_name,
        ) = self.new_all_parts = self.rename_to.split(".")
        self.ctx_key_import_scope = f"{self.rename_from}-import_scope"
        self.ctx_key_name_matcher = f"{self.rename_from}-name_matcher"
        self.ctx_key_new_func = f"{self.rename_from}-new_func"

    @property
    def name_matcher(self):
        return self.context.scratch.get(self.ctx_key_name_matcher, None)

    @property
    def new_func(self):
        return self.context.scratch.get(self.ctx_key_new_func, None)

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        """Update import statements for matching old module name."""
        return (
            self._check_import_from_exact(original_node, updated_node)
            or self._check_import_from_parent(original_node, updated_node)
            or self._check_import_from_child(updated_node)
            or updated_node
        )

    def _check_import_from_exact(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Optional[Union[BaseSmallStatement, RemovalSentinel]]:
        """
        Check for when the thing to replace is imported exactly.

        When `parent.module.the_thing` is transformed, detect such import:

            from parent.module import the_thing
        """
        # First, exit early if 'import *' is used
        if isinstance(updated_node.names, ImportStar):
            return None
        # Check whether the exact symbol is imported
        if not import_from_matches(updated_node, self.old_module_parts):
            return None
        # Match, update the node an return it
        new_import_aliases = []
        for import_alias in updated_node.names:
            if not self.old_name or import_alias.evaluated_name == self.old_name:
                if import_alias.evaluated_alias is None:
                    self.save_import_scope(original_node)
                    self.context.scratch[self.ctx_key_name_matcher] = m.Name(
                        self.old_name
                    )
                    if self.new_name:
                        self.context.scratch[self.ctx_key_new_func] = Name(
                            self.new_name
                        )
                if self.rename_from != self.rename_to:
                    if self.simple_rename:
                        AddImportsVisitor.add_needed_import(
                            context=self.context,
                            module=".".join(self.new_module_parts),
                            obj=self.new_name or import_alias.evaluated_name,
                            asname=import_alias.evaluated_alias,
                        )
                    continue
            new_import_aliases.append(import_alias)
        if not new_import_aliases:
            # Nothing left in the import statement: remove it
            return RemoveFromParent()
        # Some imports are left, update the statement
        new_import_aliases = clean_new_import_aliases(new_import_aliases)
        return updated_node.with_changes(names=new_import_aliases)

    def _check_import_from_parent(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Optional[Union[BaseSmallStatement, RemovalSentinel]]:
        """
        Check for when the parent module of thing to replace is imported.

        When `parent.module.the_thing` is transformed, detect such import:

            from parent import module
        """
        # First, exit early if 'import *' is used
        if isinstance(updated_node.names, ImportStar):
            return None
        # Check whether parent module is imported
        if not import_from_matches(updated_node, self.old_parent_module_parts):
            return None
        # Match, update the node an return it
        new_import_aliases = []
        for import_alias in updated_node.names:
            if import_alias.evaluated_name == self.old_parent_name:
                self.save_import_scope(original_node)
                module_name_str = (
                    import_alias.evaluated_alias or import_alias.evaluated_name
                )
                self.context.scratch[self.ctx_key_name_matcher] = m.Attribute(
                    value=m.Name(module_name_str),
                    attr=m.Name(self.old_name),
                )
                self.context.scratch[self.ctx_key_new_func] = Attribute(
                    attr=Name(self.new_name),
                    value=Name(import_alias.evaluated_alias or self.new_parent_name),
                )
                if self.old_parent_module_parts != self.new_parent_module_parts:
                    # import statement needs updating
                    AddImportsVisitor.add_needed_import(
                        context=self.context,
                        module=".".join(self.new_parent_module_parts),
                        obj=self.new_parent_name,
                        asname=import_alias.evaluated_alias,
                    )
                    continue
            new_import_aliases.append(import_alias)
        if not new_import_aliases:
            # Nothing left in the import statement: remove it
            return RemoveFromParent()
        # Some imports are left, update the statement
        new_import_aliases = clean_new_import_aliases(new_import_aliases)
        return updated_node.with_changes(names=new_import_aliases)

    def _check_import_from_child(
        self, updated_node: ImportFrom
    ) -> Optional[Union[BaseSmallStatement, RemovalSentinel]]:
        """
        Check import of a member of the module being codemodded.

        When `parent.module.the_thing` is transformed, detect such import:

            from parent.module.thing import something
        """
        # First, exit early if 'import *' is used
        if isinstance(updated_node.names, ImportStar):
            return None
        # Check whether a member of the module is imported
        if not import_from_matches(updated_node, self.old_all_parts):
            return None
        # Match, add import for all imported names and remove the existing import
        for import_alias in updated_node.names:
            AddImportsVisitor.add_needed_import(
                context=self.context,
                module=".".join(self.new_all_parts),
                obj=import_alias.evaluated_name,
                asname=import_alias.evaluated_alias,
            )
        return RemoveFromParent()

    def resolve_parent_node(self, node: CSTNode) -> CSTNode:
        parent_nodes = self.context.wrapper.resolve(ParentNodeProvider)  # type: ignore
        return parent_nodes[node]

    def resolve_scope(self, node: CSTNode) -> Scope:
        scopes_map = self.context.wrapper.resolve(ScopeProvider)  # type: ignore
        return scopes_map[node]  # type: ignore

    def save_import_scope(self, import_from: ImportFrom) -> None:
        scope = self.resolve_scope(import_from)
        self.context.scratch[self.ctx_key_import_scope] = scope

    @property
    def import_scope(self) -> Optional[Scope]:
        return self.context.scratch.get(self.ctx_key_import_scope, None)

    def leave_Name(self, original_node: Name, updated_node: Name) -> BaseExpression:
        """Rename reference to the imported name."""
        matcher = self.name_matcher
        if (
            matcher
            and m.matches(updated_node, matcher)
            and not self.is_wrapped_in_call(original_node)
            and self.matches_import_scope(original_node)
        ):
            return updated_node.with_changes(value=self.new_name)
        return super().leave_Name(original_node, updated_node)

    def leave_Attribute(
        self, original_node: Attribute, updated_node: Attribute
    ) -> BaseExpression:
        matcher = self.name_matcher
        if (
            matcher
            and m.matches(updated_node, matcher)
            and not self.is_wrapped_in_call(original_node)
            and self.matches_import_scope(original_node)
        ):
            return updated_node.with_changes(
                value=Name(self.new_parent_name),
                attr=Name(self.new_name),
            )
        return super().leave_Attribute(original_node, updated_node)

    def is_wrapped_in_call(self, node: CSTNode) -> bool:
        """Check whether given node is wrapped in Call."""
        parent = self.resolve_parent_node(node)
        return m.matches(parent, m.Call())

    def matches_import_scope(self, node: CSTNode) -> bool:
        """Check whether given node matches the scope of the import."""
        try:
            scope = self.resolve_scope(node)
        except KeyError:
            # Can't resolve scope of node -> consider no match
            # Might be because of one of these reasons:
            # - It's the same name in another scope
            # - It's a attribute with the same name
            # - It's a keyword argument
            return False
        return scope == self.import_scope


def clean_new_import_aliases(
    import_aliases: List[ImportAlias],
) -> List[ImportAlias]:
    """Clean up a list of import aliases."""
    # Sort them
    cleaned_import_aliases = sorted(import_aliases, key=lambda n: n.evaluated_name)
    # Remove any trailing commas
    last_name = cleaned_import_aliases[-1]
    if last_name.comma != MaybeSentinel.DEFAULT:
        cleaned_import_aliases[-1] = last_name.with_changes(comma=MaybeSentinel.DEFAULT)
    return cleaned_import_aliases


class BaseFuncRenameTransformer(BaseRenameTransformer, ABC):
    """Base class to help rename or move a function."""

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        matcher = self.name_matcher
        if m.matches(updated_node, m.Call(func=matcher)):
            return self.update_call(updated_node=updated_node)
        return super().leave_Call(original_node, updated_node)

    def update_call(self, updated_node: Call) -> BaseExpression:
        updated_args = self.update_call_args(updated_node)
        return updated_node.with_changes(args=updated_args, func=self.new_func)

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        return node.args
