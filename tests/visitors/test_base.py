from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer

from .base import BaseVisitorTest


class SameModuleRenameTransformer(BaseSimpleFuncRenameTransformer):
    """Simple transformer renaming function from same module."""

    rename_from = "django.dummy.module.func"
    rename_to = "django.dummy.module.better_func"


class TestSimpleFuncRenameTransformer(BaseVisitorTest):

    transformer = SameModuleRenameTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.dummy.module import func

            result = func()
        """
        after = """
            from django.dummy.module import better_func

            result = better_func()
        """
        self.assertCodemod(before, after)

    def test_already_imported(self) -> None:
        """Function to modify is already imported with an alias."""
        before = """
            from django.dummy.module import func, better_func

            result = func(content)
        """
        after = """
            from django.dummy.module import better_func

            result = better_func(content)
        """
        self.assertCodemod(before, after)

    def test_import_with_alias(self) -> None:
        """Function to modify is imported with an alias."""
        before = """
            from django.dummy.module import func as aliased_func

            result = aliased_func()
        """
        after = """
            from django.dummy.module import better_func as aliased_func

            result = aliased_func()
        """
        self.assertCodemod(before, after)

    def test_same_name_function(self) -> None:
        """Should not be fooled by a function bearing the same name."""
        before = """
            from utils.helpers import func

            result = func()
        """
        after = """
            from utils.helpers import func

            result = func()
        """
        self.assertCodemod(before, after)

    def test_same_name_with_alias_import_function(self) -> None:
        """Imported with alias and other function with the same name."""
        before = """
            from django.dummy.module import func as aliased_func
            from utils.helpers import func

            result = func()
            aliased_func()
        """
        after = """
            from utils.helpers import func
            from django.dummy.module import better_func as aliased_func

            result = func()
            aliased_func()
        """
        self.assertCodemod(before, after)

    def test_extra_trailing_comma_when_last(self) -> None:
        """Extra trailing comma when removed import is the last one."""
        before = """
            from django.dummy.module import better_func, func

            result = func(content)
        """
        after = """
            from django.dummy.module import better_func

            result = better_func(content)
        """
        self.assertCodemod(before, after)

    def test_parse_call_no_value(self) -> None:
        """Bug with function call without name."""
        before = """
            factory()()
        """
        after = """
            factory()()
        """
        self.assertCodemod(before, after)

    def test_lambda_no_value(self) -> None:
        """Bug with lambda call without name."""
        before = """
            (lambda x: x)(something)
        """
        after = """
            (lambda x: x)(something)
        """
        self.assertCodemod(before, after)


class OtherModuleRenameTransformer(BaseSimpleFuncRenameTransformer):
    """Transformer with different module."""

    rename_from = "django.dummy.module.func"
    rename_to = "django.better.dummy.better_func"


class TestOtherModuleRenameTransformer(BaseVisitorTest):

    transformer = OtherModuleRenameTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.dummy.module import func

            result = func()
        """
        after = """
            from django.better.dummy import better_func

            result = better_func()
        """
        self.assertCodemod(before, after)

    def test_already_imported(self) -> None:
        before = """
            from django.dummy.module import func
            from django.better.dummy import better_func

            result = func(content)
        """
        after = """
            from django.better.dummy import better_func

            result = better_func(content)
        """
        self.assertCodemod(before, after)

    def test_import_with_alias(self) -> None:
        before = """
            from django.dummy.module import func as aliased_func

            result = aliased_func()
        """
        after = """
            from django.better.dummy import better_func as aliased_func

            result = aliased_func()
        """
        self.assertCodemod(before, after)
