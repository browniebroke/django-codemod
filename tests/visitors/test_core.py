from django_codemod.visitors import URLResolversTransformer
from tests.visitors.base import BaseVisitorTest


class TestURLResolversTransformer(BaseVisitorTest):

    transformer = URLResolversTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.core.urlresolvers import path

            result = path('foo/', ...)
        """
        after = """
            from django.urls import path

            result = path('foo/', ...)
        """
        self.assertCodemod(before, after)
