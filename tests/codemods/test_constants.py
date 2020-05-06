from libcst.codemod import CodemodTest

from django_codemod.codemods import ConvertConstantCommand


class TestConvertConstantCommand(CodemodTest):

    # The codemod that will be instantiated for us in assertCodemod.
    TRANSFORM = ConvertConstantCommand

    def test_noop(self) -> None:
        before = """
            foo = "bar"
        """
        after = """
            foo = "bar"
        """

        # Verify that if we don't have a valid string match, we don't make
        # any substitutions.
        self.assertCodemod(before, after, string="baz", constant="BAZ")

    def test_substitution(self) -> None:
        before = """
            foo = "bar"
        """
        after = """
            from utils.constants import BAR

            foo = BAR
        """

        # Verify that if we do have a valid string match, we make a substitution
        # as well as import the constant.
        self.assertCodemod(before, after, string="bar", constant="BAR")
