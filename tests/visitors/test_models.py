import pytest
from parameterized import parameterized

from django_codemod.visitors.models import (
    ModelsPermalinkTransformer,
    NullBooleanFieldTransformer,
    OnDeleteTransformer,
    QuerySetDateFieldTransformer,
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
                user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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
                user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
        """
        self.assertCodemod(before, after)

    def test_multiple_kwargs_with_on_delete(self) -> None:
        """Should do nothing."""
        before = """
            from django.db import models

            class MyModel(models.Model):
                operations = [
                    migrations.CreateModel(
                        fields=[
                            (
                                'model',
                                models.OneToOneField(
                                    to='random.Model', on_delete=models.CASCADE),
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
                                    to='random.Model', on_delete=models.CASCADE),
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
                        on_delete=models.CASCADE),
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

            models.OneToOneField('model', on_delete=models.CASCADE)
        """
        self.assertCodemod(before, after)

    def test_positional_args_with_on_delete(self) -> None:
        """Should do nothing."""
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
                                on_delete=models.CASCADE),
                            ),
                        ],
                    )
                ]
        """
        self.assertCodemod(before, after)


class TestAvailableAttrsTransformer(BaseVisitorTest):
    transformer = ModelsPermalinkTransformer

    @parameterized.expand(
        [
            ("from django.db import *",),
            ("from django.db.models import *",),
        ]
    )
    def test_noop_import_star(self, import_str: str) -> None:
        """Should not try to replace if import star is used."""
        before = after = f"""
            {import_str}

            class MyModel(models.Model):

                @models.permalink
                def url(self):
                    return ('guitarist_detail', [self.slug])

                def get_name(self):
                    return get_name_from(self)
        """
        self.assertCodemod(before, after)

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


class TestNullBooleanFieldTransformer(BaseVisitorTest):
    transformer = NullBooleanFieldTransformer

    def test_noop_models(self) -> None:
        before = after = """
            from django.db import models

            class MyThing(models.Model):
                is_active = models.BooleanField()
        """
        self.assertCodemod(before, after)

    def test_noop_fields(self) -> None:
        before = after = """
            from django.db.models import BooleanField, Model

            class MyThing(Model):
                is_active = BooleanField()
        """
        self.assertCodemod(before, after)

    @pytest.mark.usefixtures("parent_module_import_enabled")
    def test_simple_substitution(self) -> None:
        before = """
            from django.db import models

            class MyThing(models.Model):
                is_active = models.NullBooleanField()
        """
        after = """
            from django.db import models

            class MyThing(models.Model):
                is_active = models.BooleanField(null=True)
        """
        self.assertCodemod(before, after)


class TestQuerySetDateFieldTransformer(BaseVisitorTest):
    transformer = QuerySetDateFieldTransformer

    @parameterized.expand([("earliest",), ("latest",)])
    def test_literal_field(self, method):
        self.assertCodemod(
            f"result = Article.objects.{method}(field_name='pub_date')",
            f"result = Article.objects.{method}('pub_date')",
        )

    def test_chained_multiline_call(self):
        self.assertCodemod(
            """
            result = Article.objects.filter(published=True).latest(
                field_name = "pub_date",  # Keep the field comment.
            )
            """,
            """
            result = Article.objects.filter(published=True).latest(
                "pub_date",  # Keep the field comment.
            )
            """,
        )

    @parameterized.expand(
        [
            ("qs.latest()",),
            ("qs.earliest('pub_date')",),
            ("qs.in_bulk(field_name='slug')",),
            ("latest(field_name='pub_date')",),
            ("qs.latest(**kwargs)",),
            ("qs.latest('pub_date', field_name='created')",),
        ]
    )
    def test_other_calls_unchanged(self, source):
        self.assertCodemod(source, source)

    @parameterized.expand(
        [
            (extra_args, value)
            for extra_args in ("", "'other', ", "**kwargs, ")
            for value in (
                "None",
                "field",
                "get_field()",
                "b'pub_date'",
                "f'{field}'",
                "'pub_' f'{field}'",
                "b'pub_' b'date'",
            )
        ]
    )
    def test_non_literal_requires_review(self, extra_args, value):
        source = f"qs.latest({extra_args}field_name={value})"
        self.assertCodemod(
            source,
            source,
            expected_warnings=[
                "Cannot safely rewrite non-literal field_name in earliest()/latest(); "
                "review this call manually."
            ],
        )

    @parameterized.expand([("earliest",), ("latest",)])
    def test_adjacent_literal_strings(self, method):
        self.assertCodemod(
            f"qs.{method}(field_name=('pub_' 'date'))",
            f"qs.{method}(('pub_' 'date'))",
        )

    @parameterized.expand(
        [
            (" # Before the equals.\n    =",),
            ("= # After the equals.\n    ",),
            (" # Before.\n    = # After.\n    ",),
            ("=\n    # On its own line.\n    ",),
            ("=\n    ",),
        ]
    )
    def test_multiline_keyword_requires_review(self, equal):
        source = f"qs.latest(field_name{equal}'pub_date')"
        self.assertCodemod(
            source,
            source,
            expected_warnings=[
                "Cannot safely rewrite field_name with comments or line breaks "
                "around '=' in earliest()/latest(); review this call manually."
            ],
        )
