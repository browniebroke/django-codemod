# Welcome to Django Codemod's documentation!

A tool to help upgrade Django projects to newer version of the framework
by automatically fixing deprecations.

**The problem**

When maintaining a Django site, over time you'll find yourself to a point where you'll need to update to the next major version of Django. When Django APIs changes, functions move or are removed, changing usages in your project might add up to many changes. Often these changes are simple to do, but sometimes a simple "find and replace" is not possible.

Take, for instance, the removal of the `url()` function from Django 4.0, to be replaced by `re_path()`. In simple cases, you might even want to switch to `path()`, which has a nicer API. A typical Django project easily has 100's or routes, so this simple decision becomes a much longer task when to be made for each of them.

**This solution**

This project solves this problem by providing codemodders for simple changes like this. A codemodder re-writes your code from the old way to the new way.

With the help of AST analysis, we're able to understand what modifications are applicable, remove imports as they become irrelevant, and add missing ones as they are needed.

To continue the example, the tool will look at the route in the `url()` call, and decide whether the regular expression may be replaced by one of the built-in URL converters and use `path()` or stick to a regex and use `re_path()`.

Interested? Check out the next sections for {ref}`installation <installation>` and {ref}`usage <usage>`.

```{toctree}
:caption: User Guide
:maxdepth: 2

installation
usage
codemods
```

```{toctree}
:caption: Project Info
:maxdepth: 2

contributing
changelog
```
