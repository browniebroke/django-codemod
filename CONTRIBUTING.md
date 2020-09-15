# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/browniebroke/django-codemod/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with
"enhancement" and "help wanted" is open to whoever wants to
implement it.

### Write Documentation

Django Codemod could always use more documentation, whether as part of the official Django Codemod docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/browniebroke/django-codemod/issues>.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `django_codemod`
for local development.

1.  Fork the `django_codemod` repo on GitHub.

2.  Clone your fork locally:

    ```shell
    $ git clone git@github.com:your_name_here/django-codemod.git
    ```

3.  Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

    ```shell
    $ mkvirtualenv django_codemod
    $ cd django-codemod/
    $ python setup.py develop
    ```

4.  Create a branch for local development:

    ```shell
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

5.  When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with
    tox:

    ```shell
    $ flake8 django_codemod tests
    $ pytest
    $ tox
    ```

    To get flake8 and tox, pip install them into your virtualenv.

6.  Commit your changes and push your branch to GitHub:

    ```shell
    $ git add .
    $ git commit -m "feat(something): your detailed description of your changes"
    $ git push origin name-of-your-bugfix-or-feature
    ```
    
    Note: the commit message should follow [the conventional commits guidelines](https://www.conventionalcommits.org), this is to enable the automation of releases. We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) which will validate the commit messages.

7.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.rst.
3.  The pull request should work for Python 3.6, 3.7 and 3.8. Check the build on Github and make sure that the tests pass for all supported Python versions.

## Deploying

The deployment should be automated and can be triggered from the Semantic Release workflow in Github. The next version will be based on [the commit logs](https://python-semantic-release.readthedocs.io/en/latest/commit-log-parsing.html#commit-log-parsing). This is done by [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/index.html) via a Github action.
