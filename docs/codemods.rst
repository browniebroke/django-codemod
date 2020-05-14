List of codemodders
===================

If everything is setup properly, the list of Django Codemods should appear when running libCST's ``list`` command:

bash::

    > python3 -m libcst.tool list
    django_30.Django30Command - Resolve deprecations for removals in Django 3.0.
    django_40.Django40Command - Resolve deprecations for removals in Django 4.0.

Codemodders are organised following the Django `deprecation timeline page`_, listing all its deprecations by version.

For instance, to fix a deprecation listed in the 4.0 section, the corresponding codemodder would be found under ``django_40``.

.. _deprecation timeline page: https://docs.djangoproject.com/en/3.0/internals/deprecation/

Django 3.0
----------

These codemodders should fix things `removed in Django 3.0`_.

.. _removed in Django 3.0: https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-0

.. automodule:: django_codemod.commands.django_30
    :members:

Django 3.1
----------

These codemodders should fix things `removed in Django 3.1`_.

.. _removed in Django 3.1: https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-1

.. automodule:: django_codemod.commands.django_31
    :members:

Django 3.2
----------

These codemodders should fix things `removed in Django 3.2`_.

.. _removed in Django 3.2: https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-2

.. automodule:: django_codemod.commands.django_32
    :members:

Django 4.0
----------

These codemodders should fix things `removed in Django 4.0`_.

.. _removed in Django 4.0: https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0

.. automodule:: django_codemod.commands.django_40
    :members:
