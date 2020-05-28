Usage
=====

Via the ``djcodemod`` command
-----------------------------

This is the preferred way to use this tool, which should fit most of the
use case, via the ``djcodemod`` command line. This command will be
available after installation and is used as follows:

.. code:: shell

   $ djcodemod --deprecated-in <Django version> <path to modify>

OR

.. code:: shell

   $ djcodemod --removed-in <Django version> <path to modify>

-  The Django version is the major + minor version of Django, for
   example ``3.0``. You may specify the patch version (e.g. ``3.0.5``),
   but only the first 2 digits are considered.
-  The path may be the root of your project or a specific file. If the
   path is a directory, the tool works recursively and will look at all
   the files under it.

Using libCST
------------

Unless you already use libCST for something else, you probably don’t
need this. It is less user friendly and requires more configuration than
the CLI.

The codemodders are implemented using libCST and the library provides
commands working nicely with `libCST
codemods <https://libcst.readthedocs.io/en/latest/codemods_tutorial.html#working-with-codemods>`__.

1. If you starting from scratch and never used ``libcst`` in your
   project, generate the ``.libcst.codemod.yaml`` config file `as per
   the libCST
   docs <https://libcst.readthedocs.io/en/latest/codemods_tutorial.html?highlight=modules#setting-up-and-running-codemods>`__:

   .. code:: bash

      > python3 -m libcst.tool initialize .

   You may skip this step if the ``.libcst.codemod.yaml`` file is
   already present.

2. Edit the config to add the commands from ``django-codemod`` to your
   modules:

   .. code:: yaml

      # .libcst.codemod.yaml
      modules:
      - 'django_codemod.commands'

   This makes the codemodders from Djnago codecod discoverable by libCST

3. If everything is setup properly, the list of Django Codemods should
   appear when running libCST’s ``list`` command:

   .. code:: shell

      > python3 -m libcst.tool list
      django_codemod.Django30Command - Resolve deprecations for removals in Django 3.0.
      django_codemod.Django40Command - Resolve deprecations for removals in Django 4.0.

   Codemodders are organised following the Django `deprecation timeline
   page <https://docs.djangoproject.com/en/3.0/internals/deprecation/>`__,
   listing all its deprecations by version.

4. Run libCST with the command from ``django-codemod`` that you want to
   apply:

   .. code:: bash

      > python3 -m libcst.tool codemod django_codemod.Django40Command .

   This will apply to code modifications for all the code under ``.``
   **in place**. Make sure it’s backed up in source control!
