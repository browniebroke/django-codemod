from django_codemod.constants import DJANGO_1_8, DJANGO_1_11, DJANGO_3_1
from django_codemod.visitors.base import BaseRenameTransformer


class QueryEmptyResultSetTransformer(BaseRenameTransformer):
    """Replace `django.db.models.query.EmptyResultSet` compatibility import."""

    deprecated_in = DJANGO_1_11
    removed_in = DJANGO_3_1
    rename_from = "django.db.models.query.EmptyResultSet"
    rename_to = "django.core.exceptions.EmptyResultSet"


class SqlEmptyResultSetTransformer(BaseRenameTransformer):
    """Replace `django.db.models.sql.EmptyResultSet` compatibility import."""

    deprecated_in = DJANGO_1_11
    removed_in = DJANGO_3_1
    rename_from = "django.db.models.sql.EmptyResultSet"
    rename_to = "django.core.exceptions.EmptyResultSet"


class DatastructuresEmptyResultSetTransformer(BaseRenameTransformer):
    """Replace `django.db.models.sql.datastructures.EmptyResultSet` import."""

    deprecated_in = DJANGO_1_11
    removed_in = DJANGO_3_1
    rename_from = "django.db.models.sql.datastructures.EmptyResultSet"
    rename_to = "django.core.exceptions.EmptyResultSet"


class FieldDoesNotExistTransformer(BaseRenameTransformer):
    """Replace `django.db.models.fields.FieldDoesNotExist` compatibility import."""

    deprecated_in = DJANGO_1_8
    removed_in = DJANGO_3_1
    rename_from = "django.db.models.fields.FieldDoesNotExist"
    rename_to = "django.core.exceptions.FieldDoesNotExist"
