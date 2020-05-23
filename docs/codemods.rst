List of codemodders
===================

Here are the automatic fixes which are supported by django-codemod at this stage:

Removed in Django 3.0
---------------------

Applied by passing the ``--removed-in 3.0`` option:

- Replaces ``render_to_response()`` by ``render()`` and add ``request=None``
  as the first argument of ``render()``.
- Add the ``obj`` argument to ``InlineModelAdmin.has_add_permission()``.

Removed in Django 4.0
---------------------

Applied by passing the ``--removed-in 4.0`` option:

- Replaces ``force_text`` and ``smart_text`` from the ``django.utils.encoding`` module by ``force_str`` and ``smart_str``
- Replaces ``ugettext``, ``ugettext_lazy``, ``ugettext_noop``, ``ungettext``, and ``ungettext_lazy`` from the ``django.utils.translation`` module by their replacements, respectively ``gettext``, ``gettext_lazy``, ``gettext_noop``, ``ngettext``, and ``ngettext_lazy``.
- Replaces ``django.conf.urls.url`` by ``django.urls.re_path``
