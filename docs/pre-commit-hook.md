(pre-commit-hook)=

# Pre-commit hook

```{versionadded} 1.2.0

```

This tool can be run as pre-commit hook with [pre-commit]. Add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/browniebroke/django-codemod
  # Any tag/version (>1.2.0):
  # https://github.com/browniebroke/django-codemod/tags
  rev: v1.2.0
  hooks:
    - id: djcodemod
      # Update arguments that suits you
      args: ["run", "--deprecated-in", "3.0"]
```

Then run `pre-commit install` and you’re ready to go.

[pre-commit]: https://pre-commit.com/
