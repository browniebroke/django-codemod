from django_codemod.visitors import AbsPathTransformer
from tests.visitors.base import BaseVisitorTest


class TestAbsPathTransformer(BaseVisitorTest):

    transformer = AbsPathTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils._os import abspathu

            result = abspathu(content)
        """
        after = """
            from os.path import abspath

            result = abspath(content)
        """
        self.assertCodemod(before, after)
