from django_codemod.visitors import (
    BaseContextTransformer,
    ContextPopExceptionTransformer,
    ContextTransformer,
    RequestContextTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestBaseContextTransformer(BaseVisitorTest):
    transformer = BaseContextTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.template.base import BaseContext

            BaseContext({})
        """
        after = """
            from django.template.context import BaseContext

            BaseContext({})
        """
        self.assertCodemod(before, after)


class TestContextTransformer(BaseVisitorTest):
    transformer = ContextTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.template.base import Context

            Context({})
        """
        after = """
            from django.template.context import Context

            Context({})
        """
        self.assertCodemod(before, after)


class TestRequestContextTransformer(BaseVisitorTest):
    transformer = RequestContextTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.template.base import RequestContext

            RequestContext({})
        """
        after = """
            from django.template.context import RequestContext

            RequestContext({})
        """
        self.assertCodemod(before, after)


class TestContextPopExceptionTransformer(BaseVisitorTest):
    transformer = ContextPopExceptionTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.template.base import ContextPopException

            raise ContextPopException()
        """
        after = """
            from django.template.context import ContextPopException

            raise ContextPopException()
        """
        self.assertCodemod(before, after)
