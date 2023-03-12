from django_codemod.visitors.crypto import GetRandomStringTransformer
from tests.visitors.base import BaseVisitorTest


class TestGetRandomStringTransformer(BaseVisitorTest):
    transformer = GetRandomStringTransformer

    def test_noop_1(self) -> None:
        """Test when nothing should change."""
        before = """
        from django.utils.crypto import get_random_string

        get_random_string(16)
        """

        after = """
        from django.utils.crypto import get_random_string

        get_random_string(16)
        """

        self.assertCodemod(before, after)

    def test_noop_2(self) -> None:
        """Test when nothing should change."""
        before = """
        from django.utils.crypto import get_random_string

        get_random_string(16, allowed_chars="abc")
        """

        after = """
        from django.utils.crypto import get_random_string

        get_random_string(16, allowed_chars="abc")
        """

        self.assertCodemod(before, after)

    def test_noop_3(self) -> None:
        """Test when nothing should change."""
        before = """
        from django.utils.crypto import get_random_string

        get_random_string(length=16, allowed_chars="abc")
        """

        after = """
        from django.utils.crypto import get_random_string

        get_random_string(length=16, allowed_chars="abc")
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Test adding the length parameter."""
        before = """
        from django.utils.crypto import get_random_string

        get_random_string()
        """

        after = """
        from django.utils.crypto import get_random_string

        get_random_string(12)
        """

        self.assertCodemod(before, after)

    def test_allowed_chars_present(self) -> None:
        """Test adding the length parameter when allowed_chars is present."""
        before = """
        from django.utils.crypto import get_random_string

        get_random_string(allowed_chars="abc")
        """

        after = """
        from django.utils.crypto import get_random_string

        get_random_string(12, allowed_chars="abc")
        """

        self.assertCodemod(before, after)
