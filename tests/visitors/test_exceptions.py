from django_codemod.visitors import (
    DatastructuresEmptyResultSetTransformer,
    QueryEmptyResultSetTransformer,
    SqlEmptyResultSetTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestQueryEmptyResultSetTransformer(BaseVisitorTest):

    transformer = QueryEmptyResultSetTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.db.models.query import EmptyResultSet

            EmptyResultSet()
        """
        after = """
            from django.core.exceptions import EmptyResultSet

            EmptyResultSet()
        """
        self.assertCodemod(before, after)


class TestSqlEmptyResultSetTransformer(BaseVisitorTest):

    transformer = SqlEmptyResultSetTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.db.models.sql import EmptyResultSet

            EmptyResultSet()
        """
        after = """
            from django.core.exceptions import EmptyResultSet

            EmptyResultSet()
        """
        self.assertCodemod(before, after)


class TestDatastructuresEmptyResultSetTransformer(BaseVisitorTest):

    transformer = DatastructuresEmptyResultSetTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.db.models.sql.datastructures import EmptyResultSet

            EmptyResultSet()
        """
        after = """
            from django.core.exceptions import EmptyResultSet

            EmptyResultSet()
        """
        self.assertCodemod(before, after)
