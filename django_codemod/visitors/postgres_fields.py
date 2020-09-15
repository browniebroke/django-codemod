from django_codemod.constants import DJANGO_2_2, DJANGO_3_1
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
