import pytest
from libcst import matchers as m

from django_codemod.visitors.base import (
    BaseFuncRenameTransformer,
    BaseModuleRenameTransformer,
    module_matcher,
)

from .base import BaseVisitorTest


@pytest.mark.parametrize(
    ("parts", "expected_matcher"),
    [
        (["django"], m.Name("django")),
        (
            ["django", "contrib"],
            m.Attribute(value=m.Name("django"), attr=m.Name("contrib")),
        ),
        (
            ["django", "contrib", "admin"],
            m.Attribute(
                value=m.Attribute(value=m.Name("django"), attr=m.Name("contrib")),
                attr=m.Name("admin"),
            ),
        ),
    ],
)
def test_module_matcher(parts, expected_matcher):
    matcher = module_matcher(parts)

    # equality comparision doesn't work with matcher:
    # compare their representation seems to work
    assert repr(matcher) == repr(expected_matcher)


class SameModuleFuncRenameTransformer(BaseFuncRenameTransformer):
    """Simple transformer renaming function from same module."""

    rename_from = "django.dummy.module.func"
    rename_to = "django.dummy.module.better_func"


class TestFuncRenameTransformer(BaseVisitorTest):

    transformer = SameModuleFuncRenameTransformer

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

    def test_reference_without_call(self) -> None:
        """Replace reference of the function even is it's not called."""
        before = """
            from django.dummy.module import func

            new_func = func
        """
        after = """
            from django.dummy.module import better_func

            new_func = better_func
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


class OtherModuleFuncRenameTransformer(BaseFuncRenameTransformer):
    """Transformer with different module."""

    rename_from = "django.dummy.module.func"
    rename_to = "django.better.dummy.better_func"


class TestOtherModuleFuncRenameTransformer(BaseVisitorTest):

    transformer = OtherModuleFuncRenameTransformer

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


class OtherModuleRenameTransformer(BaseModuleRenameTransformer):
    """Simple transformer renaming function from same module."""

    rename_from = "django.dummy.module"
    rename_to = "django.dummy.other_module"


class TestModuleRenameTransformer(BaseVisitorTest):

    transformer = OtherModuleRenameTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.dummy.module import func

            result = func()
        """
        after = """
            from django.dummy.other_module import func

            result = func()
        """
        self.assertCodemod(before, after)
