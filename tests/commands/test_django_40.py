from libcst.codemod import CodemodTest

from django_codemod.commands.django_40 import (
    ForceTextToForceStrCommand,
    SmartTextToForceStrCommand,
    UGetTextToGetTextCommand,
    UGetTextLazyToGetTextLazyCommand,
    UGetTextNoopToGetTextNoopCommand,
)


class TestForceTextToForceStrCommand(CodemodTest):

    TRANSFORM = ForceTextToForceStrCommand

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import encoding

            foo = force_str("bar")
        """
        after = """
            from django import conf
            from django.utils import encoding

            foo = force_str("bar")
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.encoding import force_text

            result = force_text(content)
        """
        after = """
            from django.utils.encoding import force_str

            result = force_str(content)
        """
        self.assertCodemod(before, after)

    def test_already_imported_substitution(self) -> None:
        """Test case where force_str is already in the imports."""
        before = """
            from django.utils.encoding import force_text, force_str

            result = force_text(content)
        """
        after = """
            from django.utils.encoding import force_str

            result = force_str(content)
        """
        self.assertCodemod(before, after)

    def test_call_no_value(self) -> None:
        """Regression test for function call without name."""
        before = """
            factory()()
        """
        after = """
            factory()()
        """
        self.assertCodemod(before, after)

    def test_lambda_no_value(self) -> None:
        """Regression test for lambda call without name."""
        before = """
            (lambda x: x)(something)
        """
        after = """
            (lambda x: x)(something)
        """
        self.assertCodemod(before, after)


class TestSmartTextToForceStrCommand(CodemodTest):

    TRANSFORM = SmartTextToForceStrCommand

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import encoding

            foo = smart_str("bar")
        """
        after = """
            from django import conf
            from django.utils import encoding

            foo = smart_str("bar")
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.utils.encoding import smart_text

            result = smart_text(content)
        """
        after = """
            from django.utils.encoding import smart_str

            result = smart_str(content)
        """
        self.assertCodemod(before, after)

    def test_already_imported_substitution(self) -> None:
        """Test case where smart_str is already in the imports."""
        before = """
            from django.utils.encoding import smart_text, smart_str

            result = smart_text(content)
        """
        after = """
            from django.utils.encoding import smart_str

            result = smart_str(content)
        """
        self.assertCodemod(before, after)


class TestUGetTextToGetTextCommand(CodemodTest):

    TRANSFORM = UGetTextToGetTextCommand

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import translation

            foo = gettext("bar")
        """
        after = """
            from django import conf
            from django.utils import translation

            foo = gettext("bar")
        """

        self.assertCodemod(before, after)

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


class TestUGetTextLazyToGetTextLazyCommand(CodemodTest):

    TRANSFORM = UGetTextLazyToGetTextLazyCommand

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import translation

            foo = gettext_lazy("bar")
        """
        after = """
            from django import conf
            from django.utils import translation

            foo = gettext_lazy("bar")
        """

        self.assertCodemod(before, after)

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

    def test_already_imported_substitution(self) -> None:
        """Test case where gettext_lazy is already in the imports."""
        before = """
            from django.utils.translation import ugettext_lazy, gettext_lazy

            result = ugettext_lazy(content)
        """
        after = """
            from django.utils.translation import gettext_lazy

            result = gettext_lazy(content)
        """
        self.assertCodemod(before, after)


class TestUGetTextNoopToGetTextNoopCommand(CodemodTest):

    TRANSFORM = UGetTextNoopToGetTextNoopCommand

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

    def test_already_imported_substitution(self) -> None:
        """Test case where gettext_noop is already in the imports."""
        before = """
            from django.utils.translation import ugettext_noop, gettext_noop

            result = ugettext_noop(content)
        """
        after = """
            from django.utils.translation import gettext_noop

            result = gettext_noop(content)
        """
        self.assertCodemod(before, after)
