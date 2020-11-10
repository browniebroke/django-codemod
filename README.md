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
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
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
    <td align="center"><a href="https://browniebroke.com"><img src="https://avatars1.githubusercontent.com/u/861044?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=browniebroke" title="Code">💻</a> <a href="https://github.com/browniebroke/django-codemod/commits?author=browniebroke" title="Documentation">📖</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://akx.github.io/"><img src="https://avatars2.githubusercontent.com/u/58669?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Aarni Koskela</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=akx" title="Code">💻</a> <a href="#ideas-akx" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/browniebroke/django-codemod/commits?author=akx" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://adamj.eu/"><img src="https://avatars2.githubusercontent.com/u/857609?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Adam Johnson</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=adamchainz" title="Documentation">📖</a></td>
    <td align="center"><a href="https://sobolevn.me"><img src="https://avatars1.githubusercontent.com/u/4660275?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Nikita Sobolev</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=sobolevn" title="Documentation">📖</a></td>
    <td align="center"><a href="http://www.zapier.com"><img src="https://avatars3.githubusercontent.com/u/21158438?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Chris VanderKolk</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/commits?author=cvanderkolk" title="Code">💻</a></td>
    <td align="center"><a href="https://ghuser.io/jayvdb"><img src="https://avatars1.githubusercontent.com/u/15092?v=4?s=80" width="80px;" alt=""/><br /><sub><b>John Vandenberg</b></sub></a><br /><a href="https://github.com/browniebroke/django-codemod/issues?q=author%3Ajayvdb" title="Bug reports">🐛</a> <a href="https://github.com/browniebroke/django-codemod/commits?author=jayvdb" title="Code">💻</a></td>
    <td align="center"><a href="https://iamshnoo.github.io/blog/"><img src="https://avatars1.githubusercontent.com/u/45921510?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Anjishnu</b></sub></a><br /><a href="#infra-iamshnoo" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
