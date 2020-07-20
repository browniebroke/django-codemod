from libcst import Arg, BaseExpression, Call, Name, SimpleString
from libcst import matchers as m
from libcst.codemod.visitors import AddImportsVisitor

from django_codemod.constants import DJANGO_3_0, DJANGO_4_0
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class URLTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.conf.urls.url``."""

    deprecated_in = DJANGO_3_0
    removed_in = DJANGO_4_0
    rename_from = "django.conf.urls.url"
    rename_to = "django.urls.re_path"

    def update_call(self, updated_node: Call) -> BaseExpression:
        first_arg, *other_args = updated_node.args
        if not m.matches(first_arg, m.Arg(value=m.SimpleString())):
            AddImportsVisitor.add_needed_import(
                context=self.context,
                module=".".join(self.new_module_parts),
                obj=self.new_name,
            )
            return super().update_call(updated_node)
        # Extract the URL pattern from the first argument
        pattern = first_arg.value.evaluated_value
        if "(?P" in pattern or not pattern.startswith("^") or not pattern.endswith("$"):
            # Dynamic group or not matching full path
            # Don't try to be smart and replace with `re_path`
            AddImportsVisitor.add_needed_import(
                context=self.context,
                module=".".join(self.new_module_parts),
                obj=self.new_name,
            )
            return super().update_call(updated_node)
        # The pattern has no dynamic part:
        # Replace by a route using `path()`
        AddImportsVisitor.add_needed_import(
            context=self.context, module=".".join(self.new_module_parts), obj="path",
        )
        route = pattern.lstrip("^").rstrip("$")
        updated_args = (Arg(value=SimpleString(f"'{route}'")), *other_args)
        return Call(args=updated_args, func=Name("path"))

    def add_new_import(self, new_name, as_name):
        pass
