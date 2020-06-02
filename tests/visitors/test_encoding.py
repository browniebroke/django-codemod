from django_codemod.visitors import (
    ForceTextTransformer,
    SmartTextTransformer,
    UnicodeCompatibleTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestForceTextTransformer(BaseVisitorTest):

    transformer = ForceTextTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.encoding import force_text

            result = force_text(content)
        """
        after = """
            from django.utils.encoding import force_str

            result = force_str(content)
        """
        self.assertCodemod(before, after)


class TestSmartTextTransformer(BaseVisitorTest):

    transformer = SmartTextTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.encoding import smart_text

            result = smart_text(content)
        """
        after = """
            from django.utils.encoding import smart_str

            result = smart_str(content)
        """
        self.assertCodemod(before, after)


class TestUnicodeCompatibleTransformer(BaseVisitorTest):

    transformer = UnicodeCompatibleTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.encoding import python_2_unicode_compatible

            @python_2_unicode_compatible
            class MyModel:
                pass
        """
        after = """
            from six import python_2_unicode_compatible

            @python_2_unicode_compatible
            class MyModel:
                pass
        """
        self.assertCodemod(before, after)
