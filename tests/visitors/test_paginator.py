from django_codemod.visitors import QuerySetPaginatorTransformer
from tests.visitors.base import BaseVisitorTest


class TestQuerySetPaginatorTransformer(BaseVisitorTest):

    transformer = QuerySetPaginatorTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = after = """
            from django.core.paginator import Paginator

            paginator_instance = Paginator([], 5)
        """

        self.assertCodemod(before, after)

    def test_instance_replacement(self) -> None:
        """Replace instantiation of the class."""
        before = """
            from django.core.paginator import QuerySetPaginator

            paginator_instance = QuerySetPaginator([], 5)
        """
        after = """
            from django.core.paginator import Paginator

            paginator_instance = Paginator([], 5)
        """

        self.assertCodemod(before, after)

    def test_reference_replacement(self) -> None:
        """Replace simple reference to the class."""
        before = """
            from django.core.paginator import QuerySetPaginator

            paginator_class = QuerySetPaginator
        """
        after = """
            from django.core.paginator import Paginator

            paginator_class = Paginator
        """

        self.assertCodemod(before, after)
