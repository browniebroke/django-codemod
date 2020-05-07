from libcst.codemod import CodemodTest

from django_codemod.codemods.django_40 import ForceTextToStrCommand


class TestForceTextToStrCommand(CodemodTest):

    TRANSFORM = ForceTextToStrCommand

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import encoding

            foo = force_str("bar")
        """
        after = """
            from django import conf
            from django.utils import encoding

            foo = force_str("bar")
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.encoding import force_text

            result = force_text(content)
        """
        after = """
            from django.utils.encoding import force_str

            result = force_str(content)
        """
        self.assertCodemod(before, after)

    def test_str_already_imported_substitution(self) -> None:
        """Test case where force_str is already in the imports."""
        before = """
            from django.utils.encoding import force_text, force_str

            result = force_text(content)
        """
        after = """
            from django.utils.encoding import force_str

            result = force_str(content)
        """
        self.assertCodemod(before, after)

    def test_call_no_value(self) -> None:
        """Regression test for function call without name."""
        before = """
            factory()()
        """
        after = """
            factory()()
        """
        self.assertCodemod(before, after)

    def test_lambda_no_value(self) -> None:
        """Regression test for lambda call without name."""
        before = """
            (lambda x: x)(something)
        """
        after = """
            (lambda x: x)(something)
        """
        self.assertCodemod(before, after)
