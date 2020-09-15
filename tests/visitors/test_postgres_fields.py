from django_codemod.visitors import (
    FloatRangeFormFieldTransformer,
    FloatRangeModelFieldTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestFloatRangeModelFieldTransformer(BaseVisitorTest):

    transformer = FloatRangeModelFieldTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = after = """
            from django.contrib.postgres.fields import DecimalRangeField

            some_range = DecimalRangeField()
        """

        self.assertCodemod(before, after)

    def test_basic_replacement(self) -> None:
        """Test simple replacement."""
        before = """
            from django.contrib.postgres.fields import FloatRangeField

            some_range = FloatRangeField()
        """
        after = """
            from django.contrib.postgres.fields import DecimalRangeField

            some_range = DecimalRangeField()
        """

        self.assertCodemod(before, after)


class TestFloatRangeFormFieldTransformer(BaseVisitorTest):

    transformer = FloatRangeFormFieldTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = after = """
            from django.contrib.postgres.forms import DecimalRangeField

            some_range = DecimalRangeField()
        """

        self.assertCodemod(before, after)

    def test_basic_replacement(self) -> None:
        """Test simple replacement."""
        before = """
            from django.contrib.postgres.forms import FloatRangeField

            some_range = FloatRangeField()
        """
        after = """
            from django.contrib.postgres.forms import DecimalRangeField

            some_range = DecimalRangeField()
        """

        self.assertCodemod(before, after)
