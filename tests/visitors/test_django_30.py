from django_codemod.visitors.django_30 import (
    RenderToResponseToRenderTransformer,
    InlineHasAddPermissionsTransformer,
)
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


class TestInlineHasAddPermissionsTransformer(BaseVisitorTest):

    transformer = InlineHasAddPermissionsTransformer

    def test_noop(self) -> None:
        """Test no modification when base class doesn't match."""
        before = """
            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)

    def test_tabular_inline(self) -> None:
        """Test modification when base class is admin.TabularInline."""
        before = """
            class MyInlineInline(TabularInline):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyInlineInline(TabularInline):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    def test_admin_tabular_inline(self) -> None:
        """Test modification when base class is admin.TabularInline."""
        before = """
            class MyInlineInline(admin.TabularInline):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyInlineInline(admin.TabularInline):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    def test_stacked_inline(self) -> None:
        """Test modification when base class is StackedInline."""
        before = """
            class MyInlineInline(StackedInline):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyInlineInline(StackedInline):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    def test_admin_stacked_inline(self) -> None:
        """Test modification when base class is admin.StackedInline."""
        before = """
            class MyInlineInline(admin.StackedInline):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyInlineInline(admin.StackedInline):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    def test_context_cleared(self) -> None:
        """Test that context is cleared and doesn't leak to other classes."""
        before = """
            class MyInlineInline(admin.TabularInline):

                def has_add_permission(self, request):
                    return False


            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyInlineInline(admin.TabularInline):

                def has_add_permission(self, request, obj = None):
                    return False


            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)
