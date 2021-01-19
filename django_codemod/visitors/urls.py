from typing import Sequence

from libcst import Arg, BaseExpression, Call, Name, SimpleString
from libcst import matchers as m
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class PatternNotSupported(RuntimeError):
    pass


# A set of regex special characters sans the dash character
REGEX_SPECIALS_SANS_DASH = set("()[]{}?*+|^$\\.&~# \t\n\r\v\f")

REGEX_TO_CONVERTER = {
    "[0-9]+": "int",
    r"\d+": "int",
    ".+": "path",
    "[-a-zA-Z0-9_]+": "slug",
    r"[\w-]+": "slug",
    r"[-\w]+": "slug",
    "[^/]+": "str",
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}": "uuid",
}


class URLTransformer(BaseFuncRenameTransformer):
    """Update `django.conf.urls.url` by equivalent `path` or `re_path`."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"

    simple_rename = False

    def update_call(self, updated_node: Call) -> BaseExpression:
        """Update `url` call with either `path` or `re_path`."""
        try:
            return self.update_call_to_path(updated_node)
        except PatternNotSupported:
            # Safe fallback to re_path()
            self.add_new_import()
            return super().update_call(updated_node)

    def update_call_to_path(self, updated_node: Call):
        """Update an URL pattern to `path()` in simple cases."""
        first_arg, *other_args = updated_node.args
        self.check_not_simple_string(first_arg)
        # Extract the URL pattern from the first argument
        pattern = first_arg.value.evaluated_value
        # If we reach this point, we might be able to use `path()`
        call = self.build_path_call(pattern, other_args)
        AddImportsVisitor.add_needed_import(
            context=self.context,
            module=".".join(self.new_module_parts),
            obj="path",
        )
        return call

    def check_not_simple_string(self, first_arg: Arg):
        """Translated patterns are not supported."""
        if not m.matches(first_arg, m.Arg(value=m.SimpleString())):
            raise PatternNotSupported()

    def build_path_call(self, pattern, other_args):
        """Build the `Call` node using Django 2.0's `path()` function."""
        route = self.build_route(pattern)
        updated_args = (Arg(value=SimpleString(f"'{route}'")), *other_args)
        return Call(args=updated_args, func=Name("path"))

    def build_route(self, pattern):
        """Build route from a URL pattern."""
        stripped_pattern = pattern.lstrip("^").rstrip("$")
        route = ""
        # Parse each group
        while "(?P<" in stripped_pattern:
            route_part, stripped_pattern = self.parse_next_group(stripped_pattern)
            route += route_part
        route += stripped_pattern
        self.check_route(route)
        return route

    def parse_next_group(self, left_to_parse):
        """Extract captured group info."""
        prefix, rest = left_to_parse.split("(?P<", 1)
        group, left_to_parse = rest.split(")", 1)
        group_name, group_regex = group.split(">", 1)
        try:
            converter = REGEX_TO_CONVERTER[group_regex]
        except KeyError:
            raise PatternNotSupported("No converter found")
        return prefix + f"<{converter}:{group_name}>", left_to_parse

    def check_route(self, route):
        """Check that route doesn't contain anymore regex."""
        if set(route) & REGEX_SPECIALS_SANS_DASH:
            raise PatternNotSupported(f"Route {route} contains regex")

    def update_call_args(self, node: Call) -> Sequence[Arg]:
        """Remove keyword argument from first argument of `re_path`."""
        first_arg, *other_args = node.args
        if m.matches(first_arg, m.Arg(keyword=m.Name("regex"))):
            first_arg = Arg(value=first_arg.value)
            return (first_arg, *other_args)
        return super().update_call_args(node)
