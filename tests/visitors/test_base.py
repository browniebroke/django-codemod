import pytest
from libcst import matchers as m
from libcst.codemod import SkipFile
from parameterized import parameterized

from django_codemod.visitors.base import (
    BaseFuncRenameTransformer,
    BaseRenameTransformer,
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

    # equality comparison doesn't work with matcher:
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

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_module(self) -> None:
        before = """
            from django.dummy import module

            result = module.func()
        """
        after = """
            from django.dummy import module

            result = module.better_func()
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

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_reference_without_call(self) -> None:
        before = """
            from django.dummy import module

            new_func = module.func
        """
        after = """
            from django.dummy import module

            new_func = module.better_func
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

    def test_import_star_ignored(self) -> None:
        """Should not change anything in case of a star import."""
        before = """
            from django.dummy.module import *

            result = func()
        """
        after = """
            from django.dummy.module import *

            result = func()
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

    def test_name_from_outer_scope(self) -> None:
        """When import from outer scope has the same name as function variable."""
        before = """
            from django.dummy.module import func

            result = func()

            def something():
                func = get_func()
                return func
        """
        after = """
            from django.dummy.module import better_func

            result = better_func()

            def something():
                func = get_func()
                return func
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            ("response.func",),
            ("response.func.other",),
            ("response.func.other.one",),
        ]
    )
    def test_attribute_access(self, attribute_access) -> None:
        """When accessing an attribute that looks like the imported name."""
        before = f"""
            from django.dummy.module import func

            result = func()

            def test_something():
                response = get_response()
                assert {attribute_access} == 1
        """
        after = f"""
            from django.dummy.module import better_func

            result = better_func()

            def test_something():
                response = get_response()
                assert {attribute_access} == 1
        """
        self.assertCodemod(before, after)

    def test_kwargs(self) -> None:
        """When function is called with a kwargs bearing the same name."""
        before = """
            from django.dummy.module import func

            func()
            something(func="test")
        """
        after = """
            from django.dummy.module import better_func

            better_func()
            something(func="test")
        """
        self.assertCodemod(before, after)

    def test_avoid_try_import(self) -> None:
        before = after = """
            try:
                from django.dummy.module import func
            except:
                from django.dummy.other_module import better_func as func

            result = func()
        """
        with pytest.raises(SkipFile):
            self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_avoid_try_import_parent(self) -> None:
        before = after = """
            try:
                from django.dummy import module
            except:
                from django.dummy import other_module as module

            result = module.func()
        """
        with pytest.raises(SkipFile):
            self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_import_star(self) -> None:
        before = after = """
            from django.dummy import *

            result = module.func()
        """
        self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_import_not_matches(self) -> None:
        before = after = """
            from django.ymmud import other_module

            result = other_module.other_func()
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

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_module(self) -> None:
        before = """
            from django.dummy import module

            result = module.func()
        """
        after = """
            from django.better import dummy

            result = dummy.better_func()
        """
        self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_module_with_other(self) -> None:
        before = """
            from django.dummy import other_mod, module

            result = module.func()
        """
        after = """
            from django.dummy import other_mod
            from django.better import dummy

            result = dummy.better_func()
        """
        self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_module_import_alias(self) -> None:
        before = """
            from django.dummy import module as django_module

            result = django_module.func()
        """
        after = """
            from django.better import dummy as django_module_

            result = django_module_.better_func()
        """
        self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_module_import_alias_other_usage(self) -> None:
        before = """
            from django.dummy import module as django_module

            result = django_module.func()
            result = django_module.other_func()
        """
        after = """
            from django.dummy import module as django_module
            from django.better import dummy as django_module_

            result = django_module_.better_func()
            result = django_module.other_func()
        """
        self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_parent_module_noop(self) -> None:
        """Parent module imported, but other function used."""
        before = after = """
            from django.dummy import module

            result = module.other_func()
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


class OtherModuleRenameTransformer(BaseRenameTransformer):
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

    def test_avoid_try_import(self) -> None:
        before = after = """
            try:
                from django.dummy.module import func
            except:
                from django.dummy.other_module import better_func as func

            result = func()
        """
        with pytest.raises(SkipFile):
            self.assertCodemod(before, after)

    def test_parent_module_substitution(self) -> None:
        before = """
            from django.dummy import module

            result = module.func()
        """
        after = """
            from django.dummy import other_module

            result = other_module.func()
        """
        self.assertCodemod(before, after)
