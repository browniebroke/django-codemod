from django_codemod.visitors import (
    UGetTextLazyToGetTextLazyTransformer,
    UGetTextNoopToGetTextNoopTransformer,
    UGetTextToGetTextTransformer,
    UNGetTextLazyToNGetTextLazyTransformer,
    UNGetTextToNGetTextTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestUGetTextToGetTextTransformer(BaseVisitorTest):

    transformer = UGetTextToGetTextTransformer

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


class TestUGetTextLazyToGetTextLazyTransformer(BaseVisitorTest):

    transformer = UGetTextLazyToGetTextLazyTransformer

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


class TestUGetTextNoopToGetTextNoopTransformer(BaseVisitorTest):

    transformer = UGetTextNoopToGetTextNoopTransformer

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


class TestUNGetTextToNGetTextTransformer(BaseVisitorTest):

    transformer = UNGetTextToNGetTextTransformer

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


class TestUNGetTextLazyToNGetTextLazyTransformer(BaseVisitorTest):

    transformer = UNGetTextLazyToNGetTextLazyTransformer

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
