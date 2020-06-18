# Usage

This package provides a `djcodemod` command line tool with 2 main supported workflows:

- Prepare future upgrades by modifying code which is deprecated in a given version using the `deprecated-in` option
- Fix previous deprecated code which is removed in a given version using the `removed-in` option

## Workflows 

### Deprecations

Let's say you just updated to Django 3.0, and suddenly you're flooded with deprecations warning on your CI (you have warning enabled on CI, right?).

You want to resolve them to avoid missing another important warning. You can do so by running the following command from the root of your repo:

```bash
djcodemod --deprecated-in 3.0 .
```

### Removals

This is more a just in time operation, assuming you haven't kept up to date with deprecation warnings, and right before upgrading to a given version (let's assume Django 4.0). In this case, you should be running:

```bash
djcodemod --removed-in 4.0 .
```

## Next steps

In either case, the tool will take a few minutes and apply a set of modifications to your code to fix deprecated or removed usages of Django. This should be much faster than doing it manually and much robust than a simple find & replace.

For the list of possible modifications with their options check {ref}`the next section <list_of_codemodders>`.
