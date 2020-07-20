from libcst import Arg, BaseExpression, Call, Name, SimpleString
from libcst import matchers as m
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class PatternNotSupported(RuntimeError):
    pass


class URLTransformer(BaseFuncRenameTransformer):
    """Resolve deprecation of ``django.conf.urls.url``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"

    simple_rename = False

    def update_call(self, updated_node: Call) -> BaseExpression:
        try:
            return self.update_call_to_path(updated_node)
        except PatternNotSupported:
            self.add_new_import()
            return super().update_call(updated_node)

    def update_call_to_path(self, updated_node: Call):
        """Update an URL pattern to `path()` in simple cases."""
        first_arg, *other_args = updated_node.args
        self.check_not_simple_string(first_arg)
        # Extract the URL pattern from the first argument
        pattern = first_arg.value.evaluated_value
        self.check_dynamic_pattern(pattern)
        # If we reach this point, we can use `path()`
        AddImportsVisitor.add_needed_import(
            context=self.context, module=".".join(self.new_module_parts), obj="path",
        )
        return self.build_path_call(pattern, other_args)

    def check_not_simple_string(self, first_arg: Arg):
        """Translated patterns are not supported."""
        if not m.matches(first_arg, m.Arg(value=m.SimpleString())):
            raise PatternNotSupported()

    def check_dynamic_pattern(self, pattern):
        """Patterns with dynamic groups """
        if "(?P" in pattern or not pattern.startswith("^") or not pattern.endswith("$"):
            # Dynamic group or not matching full path
            # Don't try to be smart and replace with `re_path`
            raise PatternNotSupported()

    def build_path_call(self, pattern, other_args):
        """Build the `Call` node using Django 2.0's `path()` function."""
        route = self.build_route(pattern)
        updated_args = (Arg(value=SimpleString(f"'{route}'")), *other_args)
        return Call(args=updated_args, func=Name("path"))

    def build_route(self, pattern):
        """Build route from a URL pattern."""
        return pattern.lstrip("^").rstrip("$")
