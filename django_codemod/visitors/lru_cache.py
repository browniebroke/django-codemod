from django_codemod.constants import DJANGO_20, DJANGO_30
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class LRUCacheTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils.lru_cache.lru_cache``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_30
    rename_from = "django.utils.lru_cache.lru_cache"
    rename_to = "functools.lru_cache"
