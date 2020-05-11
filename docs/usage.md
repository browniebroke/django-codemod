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
   > python3 -m libcst.tool codemod django_40.ForceTextToForceStrCommand .
   ```

   This will apply to code modifications for all the code under `.` **in place**.
   Make sure it's backed up in source control!

## List of codemodders

If everything is setup properly, the list of Django Codemods should appear when running libCST's `list` command:

   ```bash
   > python3 -m libcst.tool list
   django_30.RenderToResponseToRenderCommand - Replaces render_to_response() by render().
   django_40.ForceTextToForceStrCommand - Replaces force_text() by force_str().
   django_40.SmartTextToForceStrCommand - Replaces smart_text() by smart_str().
   django_40.UGetTextLazyToGetTextLazyCommand - Replaces ugettext_lazy() by gettext_lazy().
   django_40.UGetTextNoopToGetTextNoopCommand - Replaces ugettext_noop() by gettext_noop().
   django_40.UGetTextToGetTextCommand - Replaces ugettext() by gettext().
   django_40.UNGetTextLazyToNGetTextLazyCommand - Replaces ungettext_lazy() by ngettext_lazy().
   django_40.UNGetTextToNGetTextCommand - Replaces ungettext() by ngettext().
   ``` 

Codemodders are organised by the version of Django where a feature is removed. Django has a [deprecation timeline page](https://docs.djangoproject.com/en/3.0/internals/deprecation/) which is listing all its deprecations. For instance, to fix a deprecation listed in the 4.0 section, the corresponding codemodder should be found under `django_40`.
