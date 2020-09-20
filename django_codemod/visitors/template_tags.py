from typing import Optional, Union

from libcst import Assign, Decorator, ImportFrom, Module, Name, RemovalSentinel
from libcst import matchers as m

from django_codemod.constants import DJANGO_1_9, DJANGO_2_0
from django_codemod.visitors.base import BaseDjCodemodTransformer, import_from_matches


class AssignmentTagTransformer(BaseDjCodemodTransformer):
    """Replace `assignment_tag` by `simple_tag`."""

    deprecated_in = DJANGO_1_9
    removed_in = DJANGO_2_0

    ctx_key_prefix = "AssignmentTagTransformer"
    ctx_key_library_call_matcher = f"{ctx_key_prefix}-library_call_matcher"
    ctx_key_decorator_matcher = f"{ctx_key_prefix}-decorator_matcher"

    @property
    def library_call_matcher(self) -> Optional[m.Call]:
        return self.context.scratch.get(self.ctx_key_library_call_matcher, None)

    @property
    def decorators_matcher(self) -> Optional[m.BaseMatcherNode]:
        return self.context.scratch.get(self.ctx_key_decorator_matcher, None)

    def leave_Module(self, original_node: Module, updated_node: Module) -> Module:
        """Clear context when leaving module."""
        self.context.scratch.pop(self.ctx_key_library_call_matcher, None)
        self.context.scratch.pop(self.ctx_key_decorator_matcher, None)
        return super().leave_Module(original_node, updated_node)

    def visit_ImportFrom(self, node: ImportFrom) -> Optional[bool]:
        """Record whether an interesting import is detected."""
        return self._check_template_imported(node) or self._check_libary_imported(node)

    def _check_template_imported(self, node: ImportFrom) -> bool:
        """Record matcher if django.template is imported."""
        if import_from_matches(node, ["django"]):
            for import_alias in node.names:
                if m.matches(import_alias, m.ImportAlias(name=m.Name("template"))):
                    # We're visiting the `from django import template` statement
                    # Get the actual name it's imported as (in case of import alias)
                    imported_name = (
                        import_alias.asname
                        and import_alias.asname.name
                        or import_alias.name
                    )
                    # Build the `Call` matcher to look out for, eg `template.Library()`
                    self.context.scratch[self.ctx_key_library_call_matcher] = m.Call(
                        func=m.Attribute(
                            attr=m.Name("Library"), value=m.Name(imported_name.value)
                        )
                    )
                    return True
        return False

    def _check_libary_imported(self, node: ImportFrom) -> bool:
        """Record matcher if django.template.Library is imported."""
        if import_from_matches(node, ["django", "template"]):
            for import_alias in node.names:
                if m.matches(import_alias, m.ImportAlias(name=m.Name("Library"))):
                    # We're visiting the `from django.template import Library` statement
                    # Get the actual name it's imported as (in case of import alias)
                    imported_name = (
                        import_alias.asname
                        and import_alias.asname.name
                        or import_alias.name
                    )
                    # Build the `Call` matcher to look out for, eg `Library()`
                    self.context.scratch[self.ctx_key_library_call_matcher] = m.Call(
                        func=m.Name(imported_name.value)
                    )
                    return True
        return False

    def visit_Assign(self, node: Assign) -> Optional[bool]:
        """Record variable name the `Library()` call is assigned to."""
        if self.library_call_matcher and m.matches(
            node,
            m.Assign(value=self.library_call_matcher),
        ):
            # Visiting a `register = template.Library()` statement
            # Get all names on the left side of the assignment
            target_names = (
                assign_target.target.value for assign_target in node.targets
            )
            # Build the decorator matchers to look out for
            target_matchers = (
                m.Decorator(
                    decorator=m.Attribute(
                        value=m.Name(name),
                        attr=m.Name("assignment_tag"),
                    )
                )
                for name in target_names
            )
            # The final matcher should match if any of the decorator matchers matches
            self.context.scratch[self.ctx_key_decorator_matcher] = m.OneOf(
                *target_matchers
            )
        return super().visit_Assign(node)

    def leave_Decorator(
        self, original_node: Decorator, updated_node: Decorator
    ) -> Union[Decorator, RemovalSentinel]:
        """Update decorator call if all conditions are met."""
        if self.decorators_matcher and m.matches(updated_node, self.decorators_matcher):
            # If we have a decorator matcher, and it matches,
            # update the node with new name
            updated_decorator = updated_node.decorator.with_changes(
                attr=Name("simple_tag")
            )
            return updated_node.with_changes(decorator=updated_decorator)
        return super().leave_Decorator(original_node, updated_node)
