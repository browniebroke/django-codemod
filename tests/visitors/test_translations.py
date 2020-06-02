from django_codemod.visitors import (
    UGetTextLazyTransformer,
    UGetTextNoopTransformer,
    UGetTextTransformer,
    UNGetTextLazyTransformer,
    UNGetTextTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestUGetTextTransformer(BaseVisitorTest):

    transformer = UGetTextTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.translation import ugettext

            result = ugettext(content)
        """
        after = """
            from django.utils.translation import gettext

            result = gettext(content)
        """
        self.assertCodemod(before, after)

    def test_import_with_alias(self) -> None:
        """Check case with a common alias."""
        before = """
            from django.utils.translation import ugettext as _

            result = _(content)
        """
        after = """
            from django.utils.translation import gettext as _

            result = _(content)
        """
        self.assertCodemod(before, after)

    def test_already_imported_substitution(self) -> None:
        """Test case where gettext is already in the imports."""
        before = """
            from django.utils.translation import ugettext, gettext

            result = ugettext(content)
        """
        after = """
            from django.utils.translation import gettext

            result = gettext(content)
        """
        self.assertCodemod(before, after)


class TestUGetTextLazyTransformer(BaseVisitorTest):

    transformer = UGetTextLazyTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.translation import ugettext_lazy

            result = ugettext_lazy(content)
        """
        after = """
            from django.utils.translation import gettext_lazy

            result = gettext_lazy(content)
        """
        self.assertCodemod(before, after)


class TestUGetTextNoopTransformer(BaseVisitorTest):

    transformer = UGetTextNoopTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import translation

            foo = gettext_noop("bar")
        """
        after = """
            from django import conf
            from django.utils import translation

            foo = gettext_noop("bar")
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.translation import ugettext_noop

            result = ugettext_noop(content)
        """
        after = """
            from django.utils.translation import gettext_noop

            result = gettext_noop(content)
        """
        self.assertCodemod(before, after)


class TestUNGetTextTransformer(BaseVisitorTest):

    transformer = UNGetTextTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.translation import ungettext

            result = ungettext(content, plural_content, count)
        """
        after = """
            from django.utils.translation import ngettext

            result = ngettext(content, plural_content, count)
        """
        self.assertCodemod(before, after)


class TestUNGetTextLazyTransformer(BaseVisitorTest):

    transformer = UNGetTextLazyTransformer

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.translation import ungettext_lazy

            result = ungettext_lazy(content, plural_content, count)
        """
        after = """
            from django.utils.translation import ngettext_lazy

            result = ngettext_lazy(content, plural_content, count)
        """
        self.assertCodemod(before, after)

    def test_import_as_alias(self) -> None:
        """Check with a common import alias."""
        before = """
            from django.utils.translation import ungettext_lazy as _

            result = _(content, plural_content, count)
        """
        after = """
            from django.utils.translation import ngettext_lazy as _

            result = _(content, plural_content, count)
        """
        self.assertCodemod(before, after)
