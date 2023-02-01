from parameterized import parameterized

from django_codemod.visitors import (
    ActionCheckboxNameTransformer,
    InlineHasAddPermissionsTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestInlineHasAddPermissionsTransformer(BaseVisitorTest):
    transformer = InlineHasAddPermissionsTransformer

    @parameterized.expand(
        [
            ("from django.contrib.admin import *", "TabularInline"),
            ("from django.contrib import *", "admin.TabularInline"),
            ("from django.contrib.admin import *", "StackedInline"),
            ("from django.contrib import *", "admin.StackedInline"),
        ]
    )
    def test_noop_import_star(self, import_line: str, base_class: str) -> None:
        before = after = f"""
            {import_line}

            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)
        """
        self.assertCodemod(before, after)

    def test_model_admin_base_class(self) -> None:
        """Doesn't modify if base class doesn't match."""
        before = after = """
            from django.contrib import admin

            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)
        """
        self.assertCodemod(before, after)

    def test_no_base_class(self) -> None:
        """Doesn't modify if there is no base class."""
        before = after = """
            from django.contrib import admin

            class MyCustomStuff:

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)
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
    def test_simple_substitution(self, import_: str, base_class: str) -> None:
        """Modification with a valid base class."""
        before = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}):

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)
        """
        after = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}):

                def has_add_permission(self, request, obj=None):
                    if somethings:
                        return False
                    return super().has_add_permission(request, obj=obj)
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
    def test_multiple_base_classes_last(self, import_: str, base_class: str) -> None:
        """Modification with multiple base classes, valid last."""
        before = f"""
            from django.contrib{import_}

            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)
        """
        after = f"""
            from django.contrib{import_}

            class MyInlineInline(InlineMixin, {base_class}):

                def has_add_permission(self, request, obj=None):
                    if somethings:
                        return False
                    return super().has_add_permission(request, obj=obj)
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
    def test_multiple_base_classes_first(self, import_: str, base_class: str) -> None:
        """Modification with multiple base classes, valid first."""
        before = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}, OtherBase):

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)
        """
        after = f"""
            from django.contrib{import_}

            class MyInlineInline({base_class}, OtherBase):

                def has_add_permission(self, request, obj=None):
                    if somethings:
                        return False
                    return super().has_add_permission(request, obj=obj)
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            ("admin.TabularInline",),
            ("admin.StackedInline",),
        ]
    )
    def test_context_cleared(self, base_class: str) -> None:
        """Test that context is cleared and doesn't leak to other classes."""
        before = f"""
            from django.contrib import admin

            class MyInlineInline({base_class}):

                def has_add_permission(self, request):
                    if somethings:
                        return False
                    return super().has_add_permission(request)


            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        after = f"""
            from django.contrib import admin

            class MyInlineInline({base_class}):

                def has_add_permission(self, request, obj=None):
                    if somethings:
                        return False
                    return super().has_add_permission(request, obj=obj)


            class MyAdmin(admin.ModelAdmin):

                def has_add_permission(self, request):
                    return False
        """
        self.assertCodemod(before, after)


class TestActionCheckboxNameTransformer(BaseVisitorTest):
    transformer = ActionCheckboxNameTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.contrib.admin import ACTION_CHECKBOX_NAME
        """
        after = """
            from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
        """
        self.assertCodemod(before, after)
