from libcst.codemod import CodemodContext, CodemodTest

from django_codemod.commands import BaseCodemodCommand
from django_codemod.visitors.base import BaseDjCodemodTransformer


class BaseVisitorTest(CodemodTest):
    """Base test to use in all visitors tests."""

    transformer: type[BaseDjCodemodTransformer]

    def TRANSFORM(  # ty: ignore[invalid-attribute-override]
        self, context: CodemodContext
    ) -> BaseCodemodCommand:
        """Create a command for the transformer under test."""
        return BaseCodemodCommand([self.transformer], context)
