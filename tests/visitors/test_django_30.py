from django_codemod.visitors.django_30 import RenderToResponseToRenderTransformer
from .base import BaseVisitorTest


class TestRenderToResponseToRenderTransformer(BaseVisitorTest):

    transformer = RenderToResponseToRenderTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django.shortcuts import get_object_or_404, render

            result = render(request, "index.html", context={})
        """
        after = """
            from django.shortcuts import get_object_or_404, render

            result = render(request, "index.html", context={})
        """

        self.assertCodemod(before, after)

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

    def test_already_imported_substitution(self) -> None:
        """Test case where render is already in the imports."""
        before = """
            from django.shortcuts import get_object_or_404, render_to_response, render

            result = render_to_response("index.html", context={})
        """
        after = """
            from django.shortcuts import get_object_or_404, render

            result = render(None, "index.html", context={})
        """
        self.assertCodemod(before, after)
