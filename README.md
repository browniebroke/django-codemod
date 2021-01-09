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

## The problem

When maintaining a Django site, over time you'll find yourself to a point where you'll need to update to the next major version of Django. When Django APIs changes, functions move or are removed, changing usages in your project might add up to many changes. Often these changes are simple to do, but sometimes a simple "find and replace" is not possible.

Take, for instance, the removal of the `url()` function from Django 4.0, to be replaced by `re_path()`. In simple cases, you might even want to switch to `path()`, which has a nicer API. A typical Django project easily has 100's or routes, so this simple decision becomes a much longer task when to be made for each of them.

### This solution

This project solves this problem by providing codemodders for simple changes like this. A codemodder re-writes your code from the old way to the new way.

With the help of AST analysis, we're able to understand what modifications are applicable, remove imports as they become irrelevant, and add missing ones as they are needed.

To continue the example, the tool will look at the route in the `url()` call, and decide whether the regular expression may be replaced by one of the built-in URL converters and use `path()` or stick to a regex and use `re_path()`.

Interested? Check out [the documentation](https://django-codemod.readthedocs.io) for usage and the full list of codemodders.

### What this tool is not

- This tool is best suited for Django sites, NOT for reusable Django applications. The project needs to target a single Django version, e.g. 3.1.x.
- You do NOT need to install this tool as part of your project dependencies, it is a CLI tool, not a Django package to be installed in your site.

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
  <tr>
    <td align="center"><a href="https://github.com/drewbrew"><img src="https://avatars1.githubusercontent.com/u/7773256?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Drew Winstel</b></sub></a><br /><a href="#ideas-drewbrew" title="Ideas, Planning, & Feedback">🤔</a></td>
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
