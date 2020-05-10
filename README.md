# Django Codemod

[![image](https://img.shields.io/pypi/v/django-codemod.svg)](https://pypi.python.org/pypi/django-codemod)
[![image](https://img.shields.io/travis/browniebroke/django-codemod.svg)](https://travis-ci.com/browniebroke/django-codemod)
[![Documentation Status](https://readthedocs.org/projects/django-codemod/badge/?version=latest)](https://django-codemod.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/browniebroke/django-codemod/shield.svg)](https://pyup.io/repos/github/browniebroke/django-codemod/)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Collections of libCST codemodder to help upgrades to newer versions of Django.

## Features

This is based on
[libCST](https://libcst.readthedocs.io/en/latest/index.html) and
implements codemods for it. This is currently very limited but the aim
is to add more for helping with upcoming deprecations.

Currently implemented:

-   `django_codemod.commands.django_40.ForceTextToForceStrCommand`:
    migrate deprecated `force_text()` function to `force_str()`.
-   `django_codemod.commands.django_40.SmartTextToForceStrCommand`:
    migrate deprecated `smart_text()` function to `smart_str()`.
-   `django_codemod.commands.django_40.UGetTextToGetTextCommand`:
    migrate deprecated `ugettext()` function to `gettext()`.
-   `django_codemod.commands.django_40.UGetTextLazyToGetTextLazyCommand`:
    migrate deprecated `ugettext_lazy()` function to `gettext_lazy()`.
-   `django_codemod.commands.django_40.UGetTextNoopToGetTextNoopCommand`:
    migrate deprecated `ugettext_noop()` function to `gettext_noop()`.
-   `django_codemod.commands.django_40.UNGetTextToNGetTextCommand`:
    migrate deprecated `ungettext()` function to `ngettext()`.
-   `django_codemod.commands.django_40.UNGetTextLazyToNGetTextLazyCommand`:
    migrate deprecated `ungettext_lazy()` function to `ngettext_lazy()`.

Not finding what you need? I\'m open to contributions, please send me a
pull request.


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
