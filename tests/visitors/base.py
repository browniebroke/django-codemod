from typing import Type

from libcst.codemod import CodemodTest

from django_codemod.commands import BaseCodemodCommand
from django_codemod.visitors.base import BaseDjCodemodTransformer


class BaseVisitorTest(CodemodTest):
    """Base test to use in all visitors tests."""

    transformer: Type[BaseDjCodemodTransformer]

    def TRANSFORM(self, context):
        """Create a command for the transformer under test."""
        return BaseCodemodCommand([self.transformer], context)
