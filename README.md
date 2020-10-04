# Django Codemod

<p align="center">
  <a href="https://github.com/browniebroke/django-codemod/actions?query=workflow%3ACI">
    <img alt="CI Status" src="https://img.shields.io/github/workflow/status/browniebroke/django-codemod/CI?label=CI&logo=github&style=flat-square">
  </a>
  <a href="https://django-codemod.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/django-codemod.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/browniebroke/django-codemod">
    <img src="https://img.shields.io/codecov/c/github/browniebroke/django-codemod.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?amp;style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/django-codemod/">
    <img src="https://img.shields.io/pypi/v/django-codemod.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPi Status">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/django-codemod.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="pyversions">
  <img src="https://img.shields.io/pypi/l/django-codemod.svg?style=flat-square" alt="license">
  <a href="https://github.com/browniebroke/django-codemod">
    <img src="https://tokei.rs/b1/github/browniebroke/django-codemod/" alt="LoC">
  </a>
</p>

A tool to help upgrade Django projects to newer version of the framework by automatically fixing deprecations.

## Installation

Install via pip (or your favourite installer):

`pip install django-codemod`

## Usage

2 main workflow are supported:

- Prepare future upgrades by modifying code which is deprecated in a given version using the `deprecated-in` option
- Fix previous deprecated code which is removed in a given version using the `removed-in` option

**1. Deprecations**

Let's say you just updated to Django 3.0, and suddenly you're flooded with deprecations warning on your CI (you have warning enabled on CI, right?).

You want to resolve them to avoid missing another important warning. You can do so by running the following command from the root of your repo:

```bash
djcodemod run --deprecated-in 3.0 .
```

**2. Removals**

This is more a just in time operation, assuming you haven't kept up to date with deprecation warnings, and right before upgrading to a given version (let's assume Django 4.0). In this case, you should be running:

```bash
djcodemod run --removed-in 4.0 .
```

### Explanations

In either case, the tool will run for a few minutes and apply a set of modifications to your code to fix deprecated or removed usages of Django. This should be much faster than doing it manually and much robust than a simple find & replace.

Check out the [documentation](https://django-codemod.readthedocs.io) for more detail on usage and the full list of codemodders.

## How it works

This is based on [libCST](https://libcst.readthedocs.io/en/latest/index.html) and implements codemods for it. This is currently very limited but the aim is to add more for helping with upcoming deprecations.

Not finding what you need? I'm open to contributions, please send me a pull request.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://browniebroke.com"><img src="https://avatars1.githubusercontent.com/u/861044?v=4" width="80px;" alt=""/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=browniebroke" title="Code">💻</a> <a href="https://github.com/browniebroke/django-codemod/issues?q=author%3Abrowniebroke" title="Bug reports">🐛</a> <a href="https://github.com/browniebroke/django-codemod/commits?author=browniebroke" title="Documentation">📖</a></td>
    <td align="center"><a href="https://adamj.eu/"><img src="https://avatars2.githubusercontent.com/u/857609?v=4" width="80px;" alt=""/><br /><sub><b>Adam Johnson</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=adamchainz" title="Documentation">📖</a></td>
    <td align="center"><a href="https://sobolevn.me"><img src="https://avatars1.githubusercontent.com/u/4660275?v=4" width="80px;" alt=""/><br /><sub><b>Nikita Sobolev</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=sobolevn" title="Documentation">📖</a></td>
    <td align="center"><a href="http://www.zapier.com"><img src="https://avatars3.githubusercontent.com/u/21158438?v=4" width="80px;" alt=""/><br /><sub><b>Chris VanderKolk</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=cvanderkolk" title="Code">💻</a></td>
    <td align="center"><a href="https://ghuser.io/jayvdb"><img src="https://avatars1.githubusercontent.com/u/15092?v=4" width="80px;" alt=""/><br /><sub><b>John Vandenberg</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/issues?q=author%3Ajayvdb" title="Bug reports">🐛</a> <a href="https://github.com/browniebroke/django-codemod/commits?author=jayvdb" title="Code">💻</a></td>
    <td align="center"><a href="https://iamshnoo.github.io/blog/"><img src="https://avatars1.githubusercontent.com/u/45921510?v=4" width="80px;" alt=""/><br /><sub><b>Anjishnu</b></sub></a><br /><a href="#infra-iamshnoo" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
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
