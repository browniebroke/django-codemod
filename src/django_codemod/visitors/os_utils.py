from django_codemod.constants import DJANGO_2_0, DJANGO_3_0
from django_codemod.visitors.base import BaseFuncRenameTransformer


class AbsPathTransformer(BaseFuncRenameTransformer):
    """Replace `django.utils._os.abspathu` by `os.path.abspath`."""

    deprecated_in = DJANGO_2_0
    removed_in = DJANGO_3_0
    rename_from = "django.utils._os.abspathu"
    rename_to = "os.path.abspath"
