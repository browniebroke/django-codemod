from django_codemod.visitors import URLResolversTransformer
from tests.visitors.base import BaseVisitorTest


class TestURLResolversTransformer(BaseVisitorTest):
    transformer = URLResolversTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.core.urlresolvers import reverse

            result = reverse('home_page')
        """
        after = """
            from django.urls import reverse

            result = reverse('home_page')
        """
        self.assertCodemod(before, after)

    def test_parent_with_other(self) -> None:
        before = """
            from django.core import serializers, urlresolvers

            result = urlresolvers.reverse('home_page')
        """
        after = """
            from django.core import serializers
            from django import urls

            result = urls.reverse('home_page')
        """
        self.assertCodemod(before, after)
