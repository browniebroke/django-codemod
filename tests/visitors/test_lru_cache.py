from django_codemod.visitors import LRUCacheTransformer
from tests.visitors.base import BaseVisitorTest


class TestLRUCacheTransformer(BaseVisitorTest):

    transformer = LRUCacheTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.lru_cache import lru_cache

            result = lru_cache(content)
        """
        after = """
            from functools import lru_cache

            result = lru_cache(content)
        """
        self.assertCodemod(before, after)
