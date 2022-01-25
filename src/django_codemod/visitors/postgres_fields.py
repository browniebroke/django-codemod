from django_codemod.constants import DJANGO_2_2, DJANGO_3_1, DJANGO_4_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class FloatRangeModelFieldTransformer(BaseFuncRenameTransformer):
    """Replace postgres' model field `FloatRangeField` by `DecimalRangeField`."""

    deprecated_in = DJANGO_2_2
    removed_in = DJANGO_3_1
    rename_from = "django.contrib.postgres.fields.FloatRangeField"
    rename_to = "django.contrib.postgres.fields.DecimalRangeField"


class FloatRangeFormFieldTransformer(BaseFuncRenameTransformer):
    """Replace postgres' form field `FloatRangeField` by `DecimalRangeField`."""

    deprecated_in = DJANGO_2_2
    removed_in = DJANGO_3_1
    rename_from = "django.contrib.postgres.forms.FloatRangeField"
    rename_to = "django.contrib.postgres.forms.DecimalRangeField"


class JSONModelFieldTransformer(BaseFuncRenameTransformer):
    """Replace postgres' JSON field with the core JSON field."""

    deprecated_in = DJANGO_3_1
    removed_in = DJANGO_4_0
    rename_from = "django.contrib.postgres.fields.JSONField"
    rename_to = "django.db.models.JSONField"
