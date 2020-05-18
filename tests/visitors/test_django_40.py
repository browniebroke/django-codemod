from django_codemod.visitors.django_40 import (
    ForceTextToForceStrTransformer,
    SmartTextToForceStrTransformer,
    UGetTextLazyToGetTextLazyTransformer,
    UGetTextNoopToGetTextNoopTransformer,
    UGetTextToGetTextTransformer,
    UNGetTextLazyToNGetTextLazyTransformer,
    UNGetTextToNGetTextTransformer,
    URLToRePathTransformer,
)

from .base import BaseVisitorTest


class TestForceTextToForceStrTransformer(BaseVisitorTest):

    transformer = ForceTextToForceStrTransformer

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

    def test_extra_trailing_comma_when_last(self) -> None:
        """Extra trailing comma when removed import is the last one."""
        before = """
            from django.utils.encoding import force_str, force_text

            result = force_text(content)
        """
        after = """
            from django.utils.encoding import force_str

            result = force_str(content)
        """
        self.assertCodemod(before, after)


class TestSmartTextToForceStrTransformer(BaseVisitorTest):

    transformer = SmartTextToForceStrTransformer

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


class TestUGetTextToGetTextTransformer(BaseVisitorTest):

    transformer = UGetTextToGetTextTransformer

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


class TestUNGetTextToNGetTextTransformer(BaseVisitorTest):

    transformer = UNGetTextToNGetTextTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import translation

            foo = ngettext("bar", "bars", count)
        """
        after = """
            from django import conf
            from django.utils import translation

            foo = ngettext("bar", "bars", count)
        """

        self.assertCodemod(before, after)

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

    def test_already_imported_substitution(self) -> None:
        """Test case where ngettext is already in the imports."""
        before = """
            from django.utils.translation import ungettext, ngettext

            result = ungettext(content, plural_content, count)
        """
        after = """
            from django.utils.translation import ngettext

            result = ngettext(content, plural_content, count)
        """
        self.assertCodemod(before, after)


class TestUNGetTextLazyToNGetTextLazyTransformer(BaseVisitorTest):

    transformer = UNGetTextLazyToNGetTextLazyTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django import conf
            from django.utils import translation

            foo = ngettext_lazy("bar", "bars", count)
        """
        after = """
            from django import conf
            from django.utils import translation

            foo = ngettext_lazy("bar", "bars", count)
        """

        self.assertCodemod(before, after)

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

    def test_already_imported_substitution(self) -> None:
        """Test case where ngettext_lazy is already in the imports."""
        before = """
            from django.utils.translation import ungettext_lazy, ngettext_lazy

            result = ungettext_lazy(content, plural_content, count)
        """
        after = """
            from django.utils.translation import ngettext_lazy

            result = ngettext_lazy(content, plural_content, count)
        """
        self.assertCodemod(before, after)


class TestURLToRePathTransformer(BaseVisitorTest):

    transformer = URLToRePathTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = """
            from django.urls import include, re_path

            urlpatterns = [
                re_path(r'^index/$', views.index, name='index'),
                re_path(r'^weblog/', include('blog.urls')),
            ]
        """
        after = """
            from django.urls import include, re_path

            urlpatterns = [
                re_path(r'^index/$', views.index, name='index'),
                re_path(r'^weblog/', include('blog.urls')),
            ]
        """

        self.assertCodemod(before, after)

    def test_simple_substitution(self) -> None:
        """Check simple use case."""
        before = """
            from django.urls import include
            from django.conf.urls import url

            urlpatterns = [
                url(r'^index/$', views.index, name='index'),
                url(r'^weblog/', include('blog.urls')),
            ]
        """
        after = """
            from django.urls import re_path, include

            urlpatterns = [
                re_path(r'^index/$', views.index, name='index'),
                re_path(r'^weblog/', include('blog.urls')),
            ]
        """
        self.assertCodemod(before, after)

    def test_already_imported_substitution(self) -> None:
        """Test case where re_path is already in the imports."""
        before = """
            from django.urls import include, re_path
            from django.conf.urls import url

            urlpatterns = [
                url(r'^index/$', views.index, name='index'),
                re_path(r'^weblog/', include('blog.urls')),
            ]
        """
        after = """
            from django.urls import include, re_path

            urlpatterns = [
                re_path(r'^index/$', views.index, name='index'),
                re_path(r'^weblog/', include('blog.urls')),
            ]
        """
        self.assertCodemod(before, after)
