from django_codemod.constants import DJANGO_20, DJANGO_30
from django_codemod.visitors.base import BaseSimpleFuncRenameTransformer


class AbsPathTransformer(BaseSimpleFuncRenameTransformer):
    """Resolve deprecation of ``django.utils._os.abspathu``."""

    deprecated_in = DJANGO_20
    removed_in = DJANGO_30
    rename_from = "django.utils._os.abspathu"
    rename_to = "os.path.abspath"
