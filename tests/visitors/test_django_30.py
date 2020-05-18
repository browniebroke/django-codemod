from parameterized import parameterized

from django_codemod.visitors.django_30 import (
    InlineHasAddPermissionsTransformer,
    RenderToResponseToRenderTransformer,
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

    def test_model_admin_base_class(self) -> None:
        """Doesn't modify if base class doesn't match."""
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

    def test_no_base_class(self) -> None:
        """Doesn't modify if there is no base class."""
        before = """
            class MyCustomStuff:

                def has_add_permission(self, request):
                    return False
        """
        after = """
            class MyCustomStuff:

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            "TabularInline",
            "admin.TabularInline",
            "StackedInline",
            "admin.StackedInline",
        ],
    )
    def test_simple_substitution(self, base_class) -> None:
        """Modification with a valid base class."""
        before = f"""
            class MyInlineInline({base_class}):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            class MyInlineInline({base_class}):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            "TabularInline",
            "admin.TabularInline",
            "StackedInline",
            "admin.StackedInline",
        ],
    )
    def test_multiple_base_classes_last(self, base_class) -> None:
        """Modification with multiple base classes, valid last."""
        before = f"""
            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            "TabularInline",
            "admin.TabularInline",
            "StackedInline",
            "admin.StackedInline",
        ],
    )
    def test_multiple_base_classes_first(self, base_class) -> None:
        """Modification with multiple base classes, valid first."""
        before = f"""
            class MyInlineInline({base_class}, OtherBase):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            class MyInlineInline({base_class}, OtherBase):

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
