from django_codemod.constants import DJANGO_1_9, DJANGO_3_1
from django_codemod.visitors.base import BaseRenameTransformer


class PrettyNameTransformer(BaseRenameTransformer):
    """Replace `django.forms.forms.pretty_name` compatibility import."""

    deprecated_in = DJANGO_1_9
    removed_in = DJANGO_3_1
    rename_from = "django.forms.forms.pretty_name"
    rename_to = "django.forms.utils.pretty_name"


class BoundFieldTransformer(BaseRenameTransformer):
    """Replace `django.forms.forms.BoundField` compatibility import."""

    deprecated_in = DJANGO_1_9
    removed_in = DJANGO_3_1
    rename_from = "django.forms.forms.BoundField"
    rename_to = "django.forms.boundfield.BoundField"
