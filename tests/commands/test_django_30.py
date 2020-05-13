from libcst.codemod import CodemodTest

from django_codemod.commands.django_30 import (
    RenderToResponseToRenderCommand,
    Django30Command,
)


class TestRenderToResponseToRenderCommand(CodemodTest):

    TRANSFORM = RenderToResponseToRenderCommand

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


class TestDjango30Command(CodemodTest):
    TRANSFORM = Django30Command

    def test_shortcuts_substitution(self) -> None:
        """Check replacement of django.shortcuts."""
        before = """
            from django.shortcuts import render_to_response

            result = render_to_response("index.html", context={}, status=None)
        """
        after = """
            from django.shortcuts import render

            result = render(None, "index.html", context={}, status=None)
        """
        self.assertCodemod(before, after)
