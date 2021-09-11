from django_codemod.visitors import PrettyNameTransformer
from tests.visitors.base import BaseVisitorTest


class TestPrettyNameTransformer(BaseVisitorTest):

    transformer = PrettyNameTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.forms.forms import pretty_name

            pretty_name()
        """
        after = """
            from django.forms.utils import pretty_name

            pretty_name()
        """
        self.assertCodemod(before, after)
