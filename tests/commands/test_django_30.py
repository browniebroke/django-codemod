from libcst.codemod import CodemodTest

from django_codemod.commands.django_30 import Django30Command


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
