from django_codemod.visitors.decorators import (
    AvailableAttrsTransformer,
    ContextDecoratorTransformer,
)
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


class TestAvailableAttrsTransformer(BaseVisitorTest):

    transformer = AvailableAttrsTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.decorators import available_attrs

            def my_decorator(func):
                @wraps(func, assigned=available_attrs(func))
                def inner(*args, **kwargs):
                    return func(*args, **kwargs)

                return inner
        """
        after = """
            from functools import WRAPPER_ASSIGNMENTS

            def my_decorator(func):
                @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
                def inner(*args, **kwargs):
                    return func(*args, **kwargs)

                return inner
        """
        self.assertCodemod(before, after)
