from django_codemod.constants import DJANGO_2_2, DJANGO_3_1
from django_codemod.visitors.base import BaseFuncRenameTransformer


class QuerySetPaginatorTransformer(BaseFuncRenameTransformer):
    """Replace `QuerySetPaginator` class by `Paginator`."""

    deprecated_in = DJANGO_2_2
    removed_in = DJANGO_3_1
    rename_from = "django.core.paginator.QuerySetPaginator"
    rename_to = "django.core.paginator.Paginator"
