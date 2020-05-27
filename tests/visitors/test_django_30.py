from parameterized import parameterized

from django_codemod.visitors.django_30 import (
    InlineHasAddPermissionsTransformer,
    RenderToResponseToRenderTransformer,
)

from .base import BaseVisitorTest


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


class TestInlineHasAddPermissionsTransformer(BaseVisitorTest):

    transformer = InlineHasAddPermissionsTransformer

    def test_model_admin_base_class(self) -> None:
        """Doesn't modify if base class doesn't match."""
        before = """
            from django.contrib import admin

            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            from django.contrib import admin

            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)

    def test_no_base_class(self) -> None:
        """Doesn't modify if there is no base class."""
        before = """
            from django.contrib import admin

            class MyCustomStuff:

                def has_add_permission(self, request):
                    return False
        """
        after = """
            from django.contrib import admin

            class MyCustomStuff:

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            (".admin import TabularInline", "TabularInline"),
            (" import admin", "admin.TabularInline"),
            (".admin import StackedInline", "StackedInline"),
            (" import admin", "admin.StackedInline"),
        ],
    )
    def test_simple_substitution(self, import_, base_class) -> None:
        """Modification with a valid base class."""
        before = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            (".admin import TabularInline", "TabularInline"),
            (" import admin", "admin.TabularInline"),
            (".admin import StackedInline", "StackedInline"),
            (" import admin", "admin.StackedInline"),
        ],
    )
    def test_multiple_base_classes_last(self, import_, base_class) -> None:
        """Modification with multiple base classes, valid last."""
        before = f"""
            from django.contrib{import_}

            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            from django.contrib{import_}

            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            (".admin import TabularInline", "TabularInline"),
            (" import admin", "admin.TabularInline"),
            (".admin import StackedInline", "StackedInline"),
            (" import admin", "admin.StackedInline"),
        ],
    )
    def test_multiple_base_classes_first(self, import_, base_class) -> None:
        """Modification with multiple base classes, valid first."""
        before = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}, OtherBase):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}, OtherBase):

                def has_add_permission(self, request, obj = None):
                    return False
        """
        self.assertCodemod(before, after)

    def test_context_cleared(self) -> None:
        """Test that context is cleared and doesn't leak to other classes."""
        before = """
            from django.contrib import admin

            class MyInlineInline(admin.TabularInline):

                def has_add_permission(self, request):
                    return False


            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        after = """
            from django.contrib import admin

            class MyInlineInline(admin.TabularInline):

                def has_add_permission(self, request, obj = None):
                    return False


            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)
