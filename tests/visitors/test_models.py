from parameterized import parameterized

from django_codemod.visitors.models import ModelsPermalinkTransformer
from tests.visitors.base import BaseVisitorTest


class TestAvailableAttrsTransformer(BaseVisitorTest):

    transformer = ModelsPermalinkTransformer

    def test_simple_substitution_args(self) -> None:
        before = """
            from django.db import models

            class MyModel(models.Model):

                @models.permalink
                def url(self):
                    return ('guitarist_detail', [self.slug])

                def get_name(self):
                    return get_name_from(self)
        """
        after = """
            from django.db import models
            from django.urls import reverse

            class MyModel(models.Model):

                def url(self):
                    return reverse('guitarist_detail', None, [self.slug])

                def get_name(self):
                    return get_name_from(self)
        """
        self.assertCodemod(before, after)

    def test_simple_substitution_kwargs(self) -> None:
        before = """
            from django.db import models

            class MyModel(models.Model):

                @models.permalink
                def url(self):
                    return ('guitarist_detail', [], {'slug': self.slug})
        """
        after = """
            from django.db import models
            from django.urls import reverse

            class MyModel(models.Model):

                def url(self):
                    return reverse('guitarist_detail', None, [], {'slug': self.slug})
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            ("permalink", "permalink"),
            ("permalink as models_permalink", "models_permalink"),
        ]
    )
    def test_specific_import_alone(self, import_as, decorator_name) -> None:
        before = f"""
            from django.db import models
            from django.db.models import {import_as}

            class MyModel(models.Model):

                @{decorator_name}
                def url(self):
                    return ('guitarist_detail', [self.slug])
        """
        after = """
            from django.db import models
            from django.urls import reverse

            class MyModel(models.Model):

                def url(self):
                    return reverse('guitarist_detail', None, [self.slug])
        """
        self.assertCodemod(before, after)

    @parameterized.expand(
        [
            ("permalink, ObjectDoesNotExist", "permalink"),
            ("ObjectDoesNotExist, permalink", "permalink"),
            ("permalink as models_permalink, ObjectDoesNotExist", "models_permalink"),
            ("ObjectDoesNotExist, permalink as models_permalink", "models_permalink"),
        ]
    )
    def test_specific_import_with_others(self, import_as, decorator_name) -> None:
        before = f"""
            from django.db import models
            from django.db.models import {import_as}

            class MyModel(models.Model):

                @{decorator_name}
                def url(self):
                    return ('guitarist_detail', [self.slug])

                def get_name(self):
                    return 'World'
        """
        after = """
            from django.db import models
            from django.db.models import ObjectDoesNotExist
            from django.urls import reverse

            class MyModel(models.Model):

                def url(self):
                    return reverse('guitarist_detail', None, [self.slug])

                def get_name(self):
                    return 'World'
        """
        self.assertCodemod(before, after)
