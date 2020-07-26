from libcst.codemod import CodemodTest

from django_codemod.commands import BaseCodemodCommand


class BaseVisitorTest(CodemodTest):
    """Base test to use in all visitors tests."""

    transformer = None

    def TRANSFORM(self, context):
        """Create a command for the transformer under test."""
        return BaseCodemodCommand([self.transformer], context)
