from django_codemod.visitors import (
    HttpUrlQuotePlusTransformer,
    HttpUrlQuoteTransformer,
    HttpUrlUnQuotePlusTransformer,
    HttpUrlUnQuoteTransformer,
    IsSafeUrlTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestHttpUrlQuoteTransformer(BaseVisitorTest):

    transformer = HttpUrlQuoteTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.http import urlquote

            result = urlquote(content)
        """
        after = """
            from urllib.parse import quote

            result = quote(content)
        """
        self.assertCodemod(before, after)


class TestHttpUrlQuotePlusTransformer(BaseVisitorTest):

    transformer = HttpUrlQuotePlusTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.http import urlquote_plus

            result = urlquote_plus(content)
        """
        after = """
            from urllib.parse import quote_plus

            result = quote_plus(content)
        """
        self.assertCodemod(before, after)


class TestHttpUrlUnQuoteTransformer(BaseVisitorTest):

    transformer = HttpUrlUnQuoteTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.http import urlunquote

            result = urlunquote(content)
        """
        after = """
            from urllib.parse import unquote

            result = unquote(content)
        """
        self.assertCodemod(before, after)


class TestHttpUrlUnQuotePlusTransformer(BaseVisitorTest):

    transformer = HttpUrlUnQuotePlusTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.http import urlunquote_plus

            result = urlunquote_plus(content)
        """
        after = """
            from urllib.parse import unquote_plus

            result = unquote_plus(content)
        """
        self.assertCodemod(before, after)


class TestIsSafeUrlTransformer(BaseVisitorTest):

    transformer = IsSafeUrlTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.http import is_safe_url

            result = is_safe_url('http://test.com/some-path', None)
        """
        after = """
            from django.utils.http import url_has_allowed_host_and_scheme

            result = url_has_allowed_host_and_scheme('http://test.com/some-path', None)
        """
        self.assertCodemod(before, after)
