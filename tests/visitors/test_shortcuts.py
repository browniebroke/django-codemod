from django_codemod.visitors import RenderToResponseToRenderTransformer
from tests.visitors.base import BaseVisitorTest


class TestRenderToResponseToRenderTransformer(BaseVisitorTest):

    transformer = RenderToResponseToRenderTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.shortcuts import render_to_response

            result = render_to_response("index.html", context={}, status=None)
        """
        after = """
            from django.shortcuts import render

            result = render(None, "index.html", context={}, status=None)
        """
        self.assertCodemod(before, after)
