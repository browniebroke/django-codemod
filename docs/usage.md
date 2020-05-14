# Usage

Should work nicely with [libCST codemods](https://libcst.readthedocs.io/en/latest/codemods_tutorial.html#working-with-codemods).

1. If you starting from scratch and never used `libcst` in your project,
   generate the `.libcst.codemod.yaml` config file
   [as per the libCST docs](https://libcst.readthedocs.io/en/latest/codemods_tutorial.html?highlight=modules#setting-up-and-running-codemods):

   ```bash
   > python3 -m libcst.tool initialize .
   ```

   You may skip this step if the `.libcst.codemod.yaml` file is already present.

2. Edit the config to add the commands from `django-codemod` to your modules:

   ```yaml
   # .libcst.codemod.yaml
   modules:
   - 'django_codemod.commands'
   ```
   
   This makes the codemodders from Djnago codecod discoverable by libCST

3. Run libCST with the command from `django-codemod` that you want to apply:

   ```bash
   > python3 -m libcst.tool codemod Django40Command .
   ```

   This will apply to code modifications for all the code under `.` **in place**.
   Make sure it's backed up in source control!
