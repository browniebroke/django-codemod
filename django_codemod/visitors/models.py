from typing import Optional, Union

from libcst import (
    Arg,
    BaseSmallStatement,
    BaseStatement,
    Call,
    FunctionDef,
    Name,
    RemovalSentinel,
    Return,
)
from libcst import matchers as m
from libcst.codemod import ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import DJANGO_21, DJANGO_111


class ModelsPermalinkTransformer(ContextAwareTransformer):
    """Replaces ``@models.permalink`` decorator by its equivalent."""

    deprecated_in = DJANGO_111
    removed_in = DJANGO_21
    ctx_key_prefix = "ModelsPermalinkTransformer"
    ctx_key_inside_method = f"{ctx_key_prefix}-inside_method"
    _decorator_matcher = m.Decorator(
        decorator=m.Attribute(value=m.Name("models"), attr=m.Name("permalink"))
    )

    def visit_FunctionDef(self, node: FunctionDef) -> Optional[bool]:
        for decorator in node.decorators:
            if m.matches(decorator, self._decorator_matcher):
                self.context.scratch[self.ctx_key_inside_method] = True
        return super().visit_FunctionDef(node)

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> Union[BaseStatement, RemovalSentinel]:
        if self.visiting_permalink_method:
            for decorator in updated_node.decorators:
                if m.matches(decorator, self._decorator_matcher):
                    AddImportsVisitor.add_needed_import(
                        context=self.context, module="django.urls", obj="reverse",
                    )
                    updated_decorators = list(updated_node.decorators)
                    updated_decorators.remove(decorator)
                    self.context.scratch.pop(self.ctx_key_inside_method, None)
                    return updated_node.with_changes(
                        decorators=tuple(updated_decorators)
                    )
        return super().leave_FunctionDef(original_node, updated_node)

    @property
    def visiting_permalink_method(self):
        return self.context.scratch.get(self.ctx_key_inside_method, False)

    def leave_Return(
        self, original_node: Return, updated_node: Return
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if self.visiting_permalink_method and m.matches(updated_node.value, m.Tuple()):
            elem_0 = updated_node.value.elements[0]
            elem_1_3 = updated_node.value.elements[1:3]
            args = (
                Arg(elem_0.value),
                Arg(Name("None")),
                *[Arg(el.value) for el in elem_1_3],
            )
            return updated_node.with_changes(
                value=Call(func=Name("reverse"), args=args)
            )
        return super().leave_Return(original_node, updated_node)
