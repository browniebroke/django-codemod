# Usage

This package provides a `djcodemod` command line tool with 2 main supported workflows:

- Prepare future upgrades by modifying code which is deprecated in a given version using the `deprecated-in` option
- Fix previous deprecated code which is removed in a given version using the `removed-in` option

## Workflows

### Deprecations

Let's say you just updated to Django 3.0, and suddenly you're flooded with deprecations warning on your CI (you have warning enabled on CI, right?).

You want to resolve them to avoid missing another important warning. You can do so by running the following command from the root of your repo:

```bash
djcodemod run --deprecated-in 3.0 {source_file_or_directory}
```

### Removals

This is more of a just in time operation, assuming you haven't kept up to date with deprecation warnings, and right before upgrading to a given version (let's assume Django 4.0). In this case, you should be running:

```bash
djcodemod run --removed-in 4.0 {source_file_or_directory}
```

### Mix and match

Both `--deprecated-in` and `--removed-in` can be passed at once, and both accept multiple repetitions. You can also give as many source files or directory paths as you want. A more complex example might look like this:

```bash
djcodemod run --deprecated-in 3.0 --deprecated-in 3.1 --removed-in 2.2 example example1 example2/models.py settings.py
```

## Next steps

In either case, the tool will take a few minutes and apply a set of modifications to your code to fix deprecated or removed usages of Django. This should be much faster than doing it manually and much robust than a simple find & replace.

For the list of possible codemodders, you may use the `list` subcommand or check {ref}`the next section <list_of_codemodders>`.

```bash
> djcodemod list
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Codemodder          ┃ Deprecated in ┃ Removed in ┃ Description                                                ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ OnDeleteTransformer │           1.9 │        2.0 │ Add the on_delete=CASCADE to ForeignKey and OneToOneField. │
│ ...                 │           ... │        ... │                                                            │
└─────────────────────┴───────────────┴────────────┴────────────────────────────────────────────────────────────┘
```

## Files included for codemodding

The tool will only consider Python files under the given source path, ignoring files which are not tracked in git, according to rules listed in the `.gitignore` file.
