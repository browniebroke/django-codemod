from django_codemod.visitors import URLTransformer
from tests.visitors.base import BaseVisitorTest


class TestURLTransformer(BaseVisitorTest):

    transformer = URLTransformer

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
            from django.conf.urls import url
            from django.urls import include

            urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^about/$', views.about, name='about'),
                url(r'^post/(?P<slug>[w-]+)/$', views.post, name='post'),
                url(r'^weblog/', include('blog.urls')),
            ]
        """
        after = """
            from django.urls import path, re_path, include

            urlpatterns = [
                path('', views.index, name='index'),
                path('about/', views.about, name='about'),
                re_path(r'^post/(?P<slug>[w-]+)/$', views.post, name='post'),
                re_path(r'^weblog/', include('blog.urls')),
            ]
        """
        self.assertCodemod(before, after)

    def test_all_path(self) -> None:
        """Check when all can be replaced with path."""
        before = """
            from django.conf.urls import url
            from django.urls import include

            urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^about/$', views.about, name='about'),
            ]
        """
        after = """
            from django.urls import path, re_path, include

            urlpatterns = [
                path('', views.index, name='index'),
                path('about/', views.about, name='about'),
            ]
        """
        self.assertCodemod(before, after)

    def test_translated_pattern(self):
        """URL patterns can also be marked translatable."""
        before = """
            from django.urls import include
            from django.conf.urls import url
            from django.utils.translation import gettext_lazy as _

            urlpatterns = [
                url(_(r'^about/$'), views.about, name='about'),
                url(_(r'^post/(?P<slug>[w-]+)/$'), views.post, name='post'),
                url(_(r'^weblog/'), include('blog.urls')),
            ]
        """
        after = """
            from django.urls import re_path, include
            from django.utils.translation import gettext_lazy as _

            urlpatterns = [
                re_path(_(r'^about/$'), views.about, name='about'),
                re_path(_(r'^post/(?P<slug>[w-]+)/$'), views.post, name='post'),
                re_path(_(r'^weblog/'), include('blog.urls')),
            ]
        """
        self.assertCodemod(before, after)
