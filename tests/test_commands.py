from libcst.codemod import CodemodTest

from django_codemod.commands.django_codemod import Django30Command, Django40Command


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


class TestDjango40Command(CodemodTest):

    TRANSFORM = Django40Command

    def test_url_replace_substitution(self) -> None:
        """Check replacement of url()."""
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

    def test_utils_substitution(self) -> None:
        """Check replacement of django.utils."""
        before = """
            from django.utils.encoding import force_text, smart_text
            from django.utils.translation import ugettext, ugettext_lazy

            text1 = force_text(content)
            text2 = smart_text(content)
            trans1 = ugettext(content)
            trans3 = ugettext_lazy(content)
        """
        after = """
            from django.utils.encoding import force_str, smart_str
            from django.utils.translation import gettext, gettext_lazy

            text1 = force_str(content)
            text2 = smart_str(content)
            trans1 = gettext(content)
            trans3 = gettext_lazy(content)
        """
        self.assertCodemod(before, after)
