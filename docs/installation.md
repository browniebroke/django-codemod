(installation)=

# Installation

Django Codemod requires Python 3.6 or above. The preferred way to install Django Codemod, is with [pipx]:

```shell
$ pips install django-codemod
```

It will install the latest stable release in an isolated virtual environment, hence not polluting your global Python with dependencies.

If you don't have [pipx] installed, checkout [their installation instructions][pipx-install] for your operating system of choice.

## Other ways to install

Django Codemod [is published on PyPI][pypi], and is based on [libCST], therefore you may install it with `pip`, `poetry` or `pipenv` if you wish to.

[pipx]: https://pipxproject.github.io/pipx/
[pipx-install]: https://pipxproject.github.io/pipx/installation/
[pypi]: https://pypi.org/project/django-codemod/
[libcst]: https://libcst.readthedocs.io
