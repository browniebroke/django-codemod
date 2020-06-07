from django_codemod.visitors.decorators import ContextDecoratorTransformer
from tests.visitors.base import BaseVisitorTest


class TestContextDecoratorTransformer(BaseVisitorTest):

    transformer = ContextDecoratorTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.decorators import ContextDecorator

            class mycontext(ContextDecorator):
                def __enter__(self):
                    print('Starting')
                    return self

                def __exit__(self, *exc):
                    print('Finishing')
                    return False
        """
        after = """
            from contextlib import ContextDecorator

            class mycontext(ContextDecorator):
                def __enter__(self):
                    print('Starting')
                    return self

                def __exit__(self, *exc):
                    print('Finishing')
                    return False
        """
        self.assertCodemod(before, after)
