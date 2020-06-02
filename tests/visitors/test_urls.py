from django_codemod.visitors import URLToRePathTransformer
from tests.visitors.base import BaseVisitorTest


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
