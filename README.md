# Django Codemod

[![image](https://img.shields.io/pypi/v/django-codemod.svg)](https://pypi.python.org/pypi/django-codemod)
[![image](https://img.shields.io/travis/browniebroke/django-codemod.svg)](https://travis-ci.com/browniebroke/django-codemod)
[![Documentation Status](https://readthedocs.org/projects/django-codemod/badge/?version=latest)](https://django-codemod.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/browniebroke/django-codemod/shield.svg)](https://pyup.io/repos/github/browniebroke/django-codemod/)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Collections of libCST codemodder to help upgrades to newer versions of Django.

## Features

This is based on
[libCST](https://libcst.readthedocs.io/en/latest/index.html) and
implements codemods for it. This is currently very limited but the aim
is to add more for helping with upcoming deprecations.

Currently implemented codemodders are listed below and grouped
by the version of Django where deprecations are removed.

Not finding what you need? I'm open to contributions,
please send me a pull request.

### Django 4.0

All these are in the module `django_codemod.commands.django_40`:

- `ForceTextToForceStrCommand`: migrate deprecated `force_text()` function to `force_str()`.
- `SmartTextToForceStrCommand`: migrate deprecated `smart_text()` function to `smart_str()`.
- `UGetTextToGetTextCommand`: migrate deprecated `ugettext()` function to `gettext()`.
- `UGetTextLazyToGetTextLazyCommand`: migrate deprecated `ugettext_lazy()` function to `gettext_lazy()`.
- `UGetTextNoopToGetTextNoopCommand`: migrate deprecated `ugettext_noop()` function to `gettext_noop()`.
- `UNGetTextToNGetTextCommand`: migrate deprecated `ungettext()` function to `ngettext()`.
- `UNGetTextLazyToNGetTextLazyCommand`: migrate deprecated `ungettext_lazy()` function to `ngettext_lazy()`.
- `URLToRePathCommand`: migrate deprecated `url()` function to `re_path()`.

### Django 3.2

All these are in the module `django_codemod.commands.django_32`:

Nothing these yet!

### Django 3.1

All these are in the module `django_codemod.commands.django_31`:

Nothing these yet!

### Django 3.0

All these are in the module `django_codemod.commands.django_30`:

- `RenderToResponseToRenderCommand`: migrate deprecated `render_to_response()` function to `render()`.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://browniebroke.com"><img src="https://avatars1.githubusercontent.com/u/861044?v=4" width="80px;" alt=""/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=browniebroke" title="Code">💻</a> <a href="https://github.com/browniebroke/django-codemod/issues?q=author%3Abrowniebroke" title="Bug reports">🐛</a> <a href="https://github.com/browniebroke/django-codemod/commits?author=browniebroke" title="Documentation">📖</a></td>
    <td align="center"><a href="https://adamj.eu/"><img src="https://avatars2.githubusercontent.com/u/857609?v=4" width="80px;" alt=""/><br /><sub><b>Adam Johnson</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=adamchainz" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
