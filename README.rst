==============
Django Codemod
==============


.. image:: https://img.shields.io/pypi/v/django-codemod.svg
        :target: https://pypi.python.org/pypi/django-codemod

.. image:: https://img.shields.io/travis/browniebroke/django-codemod.svg
        :target: https://travis-ci.com/browniebroke/django-codemod

.. image:: https://readthedocs.org/projects/django-codemod/badge/?version=latest
        :target: https://django-codemod.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://pyup.io/repos/github/browniebroke/django-codemod/shield.svg
     :target: https://pyup.io/repos/github/browniebroke/django-codemod/
     :alt: Updates

Codemod to help upgrading to newer versions of Django.

* Free software: MIT license
* Documentation: https://django-codemod.readthedocs.io.

Features
--------

This is based on `libCST <https://libcst.readthedocs.io/en/latest/index.html>`_
and implements codemods for it. This is currently very limited but the aim is
to add more for helping with upcoming deprecations.

Currently implemented:

* ``django_codemod.codemods.django_40.ForceTextToStrCommand``: migrate deprecated
  ``focre_str()`` function to ``force_str()``.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
