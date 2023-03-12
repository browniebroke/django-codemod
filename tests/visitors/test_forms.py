from django_codemod.visitors import BoundFieldTransformer, PrettyNameTransformer
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


class TestBoundFieldTransformer(BaseVisitorTest):
    transformer = BoundFieldTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.forms.forms import BoundField

            BoundField()
        """
        after = """
            from django.forms.boundfield import BoundField

            BoundField()
        """
        self.assertCodemod(before, after)
