"""
Backport of re.escape() from Python 3.7.

The behavior changed in Python 3.7 so we need this to get a consistent
behaviour until we drop support for Python 3.6.

> Change re.escape() to only escape regex special characters instead of
> escaping all characters other than ASCII letters, numbers, and '_'.

Source: https://docs.python.org/3/whatsnew/3.7.html
"""

_special_chars_map = {i: "\\" + chr(i) for i in b"()[]{}?*+-|^$\\.&~# \t\n\r\v\f"}


def escape(pattern):
    """Escape special characters in a string."""
    return pattern.translate(_special_chars_map)
