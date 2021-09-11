from django_codemod.constants import DJANGO_1_7, DJANGO_3_1
from django_codemod.visitors.base import BaseRenameTransformer


class BaseContextTransformer(BaseRenameTransformer):
    """Replace `django.template.base.BaseContext` compatibility import."""

    deprecated_in = DJANGO_1_7
    removed_in = DJANGO_3_1
    rename_from = "django.template.base.BaseContext"
    rename_to = "django.template.context.BaseContext"


class ContextTransformer(BaseRenameTransformer):
    """Replace `django.template.base.Context` compatibility import."""

    deprecated_in = DJANGO_1_7
    removed_in = DJANGO_3_1
    rename_from = "django.template.base.Context"
    rename_to = "django.template.context.Context"


class RequestContextTransformer(BaseRenameTransformer):
    """Replace `django.template.base.RequestContext` compatibility import."""

    deprecated_in = DJANGO_1_7
    removed_in = DJANGO_3_1
    rename_from = "django.template.base.RequestContext"
    rename_to = "django.template.context.RequestContext"


class ContextPopExceptionTransformer(BaseRenameTransformer):
    """Replace `django.template.base.ContextPopException` compatibility import."""

    deprecated_in = DJANGO_1_7
    removed_in = DJANGO_3_1
    rename_from = "django.template.base.ContextPopException"
    rename_to = "django.template.context.ContextPopException"
