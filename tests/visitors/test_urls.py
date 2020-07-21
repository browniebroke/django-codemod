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
                path('weblog/', include('blog.urls')),
            ]
        """
        self.assertCodemod(before, after)

    def test_starting_caret(self) -> None:
        """Patterns not starting with '^' are migrated to re_path."""
        before = """
            from django.conf.urls import url

            urlpatterns = [
                url(r'about/$', views.about, name='about'),
            ]
        """
        after = """
            from django.urls import re_path

            urlpatterns = [
                re_path(r'about/$', views.about, name='about'),
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
            from django.urls import path, include

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

    def test_grouped_path(self) -> None:
        """Check replacing pattern with groups."""
        uuid_re = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        before = fr"""
            from django.conf.urls import url

            urlpatterns = [
                url(r'^page/(?P<number>[0-9]+)/$', views.page, name='page'),
                url(r'^page/(?P<number>\d+)/$', views.page, name='page'),
                url(r'^post/(?P<slug>[-a-zA-Z0-9_]+)/$', views.post, name='post'),
                url(r'^post/(?P<slug>[\w-]+)/$', views.post, name='post'),
                url(r'^about/(?P<name>[^/]+)/$', views.about, name='about'),
                url(r'^uuid/(?P<uuid>{uuid_re})/$', by_uuid),
                url(r'^(?P<path>.+)/$', views.default, name='default'),
            ]
        """
        after = """
            from django.urls import path

            urlpatterns = [
                path('page/<int:number>/', views.page, name='page'),
                path('page/<int:number>/', views.page, name='page'),
                path('post/<slug:slug>/', views.post, name='post'),
                path('post/<slug:slug>/', views.post, name='post'),
                path('about/<str:name>/', views.about, name='about'),
                path('uuid/<uuid:uuid>/', by_uuid),
                path('<path:path>/', views.default, name='default'),
            ]
        """
        self.assertCodemod(before, after)

    def test_non_captured_group(self) -> None:
        """Non-capturing regex should be moved to re_path."""
        before = """
            from django.conf.urls import url

            urlpatterns = [
                url(r'^page/[0-9]+/$', views.page, name='page'),
            ]
        """
        after = """
            from django.urls import re_path

            urlpatterns = [
                re_path(r'^page/[0-9]+/$', views.page, name='page'),
            ]
        """
        self.assertCodemod(before, after)
