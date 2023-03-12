from parameterized import parameterized

from django_codemod.visitors import AssignmentTagTransformer
from tests.visitors.base import BaseVisitorTest


class TestAssignmentTagTransformer(BaseVisitorTest):
    transformer = AssignmentTagTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = after = """
            from django import template

            register = template.Library()


            @register.simple_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            ("from django import contrib",),
            ("from django.template import Engine",),
        ]
    )
    def test_noop_not_imported(self, import_line: str) -> None:
        """Test when import is missing."""
        before = after = f"""
            {import_line}

            @register.assignment_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_noop_import_star(self) -> None:
        """Test when imported as star import."""
        before = after = """
            from django import *

            register = template.Library()


            @register.assignment_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Test basic substitution."""
        before = """
            from django import template

            register = template.Library()


            @register.assignment_tag
            def some_tag():
                return "Hello"
        """
        after = """
            from django import template

            register = template.Library()


            @register.simple_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_substitution_unusual_name(self) -> None:
        """Test substitution with a different name."""
        before = """
            from django import template

            lib = template.Library()


            @lib.assignment_tag
            def some_tag():
                return "Hello"
        """
        after = """
            from django import template

            lib = template.Library()


            @lib.simple_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_template_imported_alias(self) -> None:
        """Test when django.template is imported with alias."""
        before = """
            from django import template as dj_template

            register = dj_template.Library()


            @register.assignment_tag
            def some_tag():
                return "Hello"
        """
        after = """
            from django import template as dj_template

            register = dj_template.Library()


            @register.simple_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_noop_content_star_import(self) -> None:
        """Test when Library class is imported as star import."""
        before = after = """
            from django.template import *

            register = Library()


            @register.assignment_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_library_class_imported(self) -> None:
        """Test when Library class is imported."""
        before = """
            from django.template import Library

            register = Library()


            @register.assignment_tag
            def some_tag():
                return "Hello"
        """
        after = """
            from django.template import Library

            register = Library()


            @register.simple_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)

    def test_library_class_imported_with_alias(self) -> None:
        """Test when django.template is imported with alias."""
        before = """
            from django.template import Library as TmplLibrary

            register = TmplLibrary()


            @register.assignment_tag
            def some_tag():
                return "Hello"
        """
        after = """
            from django.template import Library as TmplLibrary

            register = TmplLibrary()


            @register.simple_tag
            def some_tag():
                return "Hello"
        """

        self.assertCodemod(before, after)
