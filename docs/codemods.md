(list_of_codemodders)=

# Codemodders

Here is the list of automatic fixes which are supported by `django-codemod`
at this stage. This list will be updated as new fixes are implemented.

This is also accessible via the `djcodemod list` command.

## Removed in Django 2.0

Applied by passing the `--removed-in 2.0` or `--deprecated-in 1.9` option:

- Adds the `on_delete=models.CASCADE` to all `ForeignKey` and `OneToOneField`s
  that don’t use a different option.
- Replaces template tags decorator `assignment_tag` by `simple_tag`.
- Removes the `weak` argument to `Signal.disconnect()` calls. This will only
  apply to built-in signals (`pre_save`, `post_save`, ...) and to `disconnect()`
  calls with keyword arguments.

Applied by passing the `--removed-in 2.0` or `--deprecated-in 1.10` option:

- Replaces module `django.core.urlresolvers` with `django.urls`.

## Removed in Django 2.1

Applied by passing the `--removed-in 2.1` or `--deprecated-in 1.11` option:

- Replaces the `@models.permalink` decorator by a call to `reverse()`
  in the return statement.

## Removed in Django 3.0

Applied by passing the `--removed-in 3.0` or `--deprecated-in 2.0` option:

- Replaces `render_to_response()` by `render()` and add `request=None`
  as the first argument of `render()`.
- Replaces `django.utils.lru_cache.lru_cache()` by the function it's
  an alias of: `functools.lru_cache()`.
- Replaces `django.utils._os.abspathu()` by the function it's an
  alias of: `os.path.abspath()`.
- Replaces `django.utils.encoding.python_2_unicode_compatible()` by
  the function it's an alias of: `six.python_2_unicode_compatible()`.
- Replaces `django.utils.decorators.ContextDecorator` by the class
  from the standard library it's an alias to
  `contextlib.ContextDecorator`.
- Replace `django.utils.decorators.available_attrs()` by its return
  value `functools.WRAPPER_ASSIGNMENTS`.
- Replace `HttpRequest.xreadlines()` by iterating over the request.

  This codemodder is quite conservative and will only replace function
  calls on variables or attributes called `request` or `req`.

  For example, it will fix `request.xreadlines()` or `self.request.xreadlines()`
  but not `r.xreadlines()`.

Applied by passing the `--removed-in 3.0` or `--deprecated-in 2.1` option:

- Add the `obj` argument to `InlineModelAdmin.has_add_permission()`.
- Replace `django.utils.http.cookie_date()` by `http_date()`, which follows
  the format of the latest RFC.

## Removed in Django 3.1

Applied by passing the `--removed-in 3.1` or `--deprecated-in 2.2` option:

- Replace `django.utils.timezone.FixedOffset` by `datetime.timezone`.
- Replace `django.core.paginator.QuerySetPaginator` class by `Paginator`.
- Replace the `FloatRangeField` model and form fields in
  `django.contrib.postgres` by `DecimalRangeField`.

## Removed in Django 4.0

Applied by passing the `--removed-in 4.0` or `--deprecated-in 3.0` option:

- Replaces `force_text` and `smart_text` from the
  `django.utils.encoding` module by `force_str` and `smart_str`
- Replaces `urlquote`, `urlquote_plus`, `urlunquote` and
  `urlunquote_plus` from the `django.utils.http` module by their the
  functions they alias to, respectively `quote`, `quote_plus`,
  `unquote` and `unquote_plus` from the `urllib.parse.quote` module.
- Replaces `ugettext`, `ugettext_lazy`, `ugettext_noop`, `ungettext`,
  and `ungettext_lazy` from the `django.utils.translation` module by
  their replacements, respectively `gettext`, `gettext_lazy`,
  `gettext_noop`, `ngettext`, and `ngettext_lazy`.
- Replaces `unescape_entities` from the `django.utils.text` module by
  `html.unescape` from the standard library.
- Replaces `django.conf.urls.url` by `django.urls.path` or `re_path`.
  This is quite conservative for replacements to `path` and fallback
  to `re_path` for anything non-simple.
- Replaces `django.utils.http.is_safe_url` by
  `django.utils.http.url_has_allowed_host_and_scheme`.

Applied by passing the `--removed-in 4.0` or `--deprecated-in 3.1` option:

- Replaces postgres' `JSONField` by the cross database equivalent field.
- Replaces `NullBooleanField` by `BooleanField(null=True)`.
- Add required `length` argument `django.utils.crypto.get_random_string` calls.
