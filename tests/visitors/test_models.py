from parameterized import parameterized

from django_codemod.visitors.models import (
    ModelsPermalinkTransformer,
    OnDeleteTransformer,
)
from tests.visitors.base import BaseVisitorTest


class TestOnDeleteTransformer(BaseVisitorTest):

    transformer = OnDeleteTransformer

    def test_foreign_key(self) -> None:
        before = """
            class MyModel(models.Model):
                user = models.ForeignKey('auth.User')
        """
        after = """
            from django.db import models

            class MyModel(models.Model):
                user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
        """
        self.assertCodemod(before, after)

    def test_one_to_one_field(self) -> None:
        before = """
            class MyModel(models.Model):
                user = models.OneToOneField('auth.User')
        """
        after = """
            from django.db import models

            class MyModel(models.Model):
                user = models.OneToOneField('auth.User', on_delete = models.CASCADE)
        """
        self.assertCodemod(before, after)

    def test_multiple_kwargs_with_on_delete(self) -> None:
        """ Should do nothing """
        before = """
            from django.db import models

            class MyModel(models.Model):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'model',
                                models.OneToOneField(
                                    to = 'random.Model', on_delete = models.CASCADE),
                            ),
                        ],
                    )
                ]
        """
        after = """
            from django.db import models

            class MyModel(models.Model):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'model',
                                models.OneToOneField(
                                    to = 'random.Model', on_delete = models.CASCADE),
                            ),
                        ],
                    )
                ]
        """
        self.assertCodemod(before, after)

    def test_multiple_kwargs_without_on_delete(self) -> None:
        before = """
            from django.db import models


            class MyModel(models.Model):
                operations = [
                    migrations.AddField(
                        field=models.ForeignKey(
                            related_name='model',
                            blank=True,
                            to='random.Model',
                            null=True,
                        ),
                    )
                ]
        """
        after = """
            from django.db import models


            class MyModel(models.Model):
                operations = [
                    migrations.AddField(
                        field=models.ForeignKey(
                            related_name='model',
                            blank=True,
                            to='random.Model',
                            null=True,
                        on_delete = models.CASCADE),
                    )
                ]
        """
        self.assertCodemod(before, after)

    def test_positional_args_without_on_delete(self) -> None:
        before = """
            from django.db import models

            models.OneToOneField('model')
        """
        after = """
            from django.db import models

            models.OneToOneField('model', on_delete = models.CASCADE)
        """
        self.assertCodemod(before, after)

    def test_positional_args_with_on_delete(self) -> None:
        """ Should do nothing """
        before = """
            from django.db import models


            class MyModel(models.randomModel):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'field_name',
                                models.OneToOneField(
                                    'model.Location',
                                    models.CASCADE,
                                    auto_created=True,
                                ),
                            ),
                        ],
                    )
                ]
        """
        after = """
            from django.db import models


            class MyModel(models.randomModel):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'field_name',
                                models.OneToOneField(
                                    'model.Location',
                                    models.CASCADE,
                                    auto_created=True,
                                ),
                            ),
                        ],
                    )
                ]
        """
        self.assertCodemod(before, after)

    def test_add_model_import(self) -> None:
        before = """
            from random.place import CustomModel

            class MyModel(CustomModel):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'field_name',
                                CustomModel.OneToOneField(
                                    'model.Location',
                                    auto_created=True,
                                ),
                            ),
                        ],
                    )
                ]
        """
        after = """
            from random.place import CustomModel
            from django.db import models

            class MyModel(CustomModel):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'field_name',
                                CustomModel.OneToOneField(
                                    'model.Location',
                                    auto_created=True,
                                on_delete = models.CASCADE),
                            ),
                        ],
                    )
                ]
        """
        self.assertCodemod(before, after)


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
