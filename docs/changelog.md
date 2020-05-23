# Changelog

## [Unreleased](https://github.com/browniebroke/django-codemod/tree/HEAD)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.6.0...HEAD)

### 🚀 Enhancements:

- Add a djcodemod CLI [\#55](https://github.com/browniebroke/django-codemod/pull/55) ([browniebroke](https://github.com/browniebroke))

### 🐛 Bug Fixes:

- Make sure the function to rename is imported before renaming [\#54](https://github.com/browniebroke/django-codemod/pull/54) ([browniebroke](https://github.com/browniebroke))

### 📖 Documentation updates:

- Updates README.me with proper travis badge [\#50](https://github.com/browniebroke/django-codemod/pull/50) ([sobolevn](https://github.com/sobolevn))

## [v0.6.0](https://github.com/browniebroke/django-codemod/tree/v0.6.0) (2020-05-22)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.5.0...v0.6.0)

### 🚀 Enhancements:

- Add the `obj` argument to `InlineModelAdmin.has\_add\_permission\(\)` [\#45](https://github.com/browniebroke/django-codemod/pull/45) ([browniebroke](https://github.com/browniebroke))

### 🐛 Bug Fixes:

- Fix InlineModelAdmin transformer with multiple base classes [\#46](https://github.com/browniebroke/django-codemod/pull/46) ([browniebroke](https://github.com/browniebroke))
- Fix commands non-findable by libCST [\#44](https://github.com/browniebroke/django-codemod/pull/44) ([browniebroke](https://github.com/browniebroke))
- Fix bug with trailing comma when removed import is the last one [\#39](https://github.com/browniebroke/django-codemod/pull/39) ([browniebroke](https://github.com/browniebroke))
- Fix bug with lost alias when 'import as' is used [\#38](https://github.com/browniebroke/django-codemod/pull/38) ([browniebroke](https://github.com/browniebroke))

### 🗑 Removals:

- Remove commands to fix single deprecations [\#43](https://github.com/browniebroke/django-codemod/pull/43) ([browniebroke](https://github.com/browniebroke))

## [v0.5.0](https://github.com/browniebroke/django-codemod/tree/v0.5.0) (2020-05-13)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.4.0...v0.5.0)

### 🚀 Enhancements:

- New commands to fix all deprecations for a given version of Django [\#37](https://github.com/browniebroke/django-codemod/pull/37) ([browniebroke](https://github.com/browniebroke))
- Refactor & move main logic from commands to visitors [\#36](https://github.com/browniebroke/django-codemod/pull/36) ([browniebroke](https://github.com/browniebroke))
- Refactor BaseSimpleFuncRename to simplify implementing new codemod [\#32](https://github.com/browniebroke/django-codemod/pull/32) ([browniebroke](https://github.com/browniebroke))

### 📖 Documentation updates:

- Document list of codemodders with autodoc [\#33](https://github.com/browniebroke/django-codemod/pull/33) ([browniebroke](https://github.com/browniebroke))

## [v0.4.0](https://github.com/browniebroke/django-codemod/tree/v0.4.0) (2020-05-11)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.3.0...v0.4.0)

### 🚀 Enhancements:

- Resolve deprecation for django.shortcuts.render\_to\_response\(\) [\#25](https://github.com/browniebroke/django-codemod/pull/25) ([browniebroke](https://github.com/browniebroke))

### 📖 Documentation updates:

- Add missing description for URLToRePathCommand [\#28](https://github.com/browniebroke/django-codemod/pull/28) ([browniebroke](https://github.com/browniebroke))
- Document how to list all available codemodders [\#27](https://github.com/browniebroke/django-codemod/pull/27) ([browniebroke](https://github.com/browniebroke))

## [v0.3.0](https://github.com/browniebroke/django-codemod/tree/v0.3.0) (2020-05-10)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.2.1...v0.3.0)

### 🚀 Enhancements:

- Support resolving django.conf.urls.url\(\) deprecation [\#22](https://github.com/browniebroke/django-codemod/pull/22) ([browniebroke](https://github.com/browniebroke))

### 📖 Documentation updates:

- Fix some refs in README [\#21](https://github.com/browniebroke/django-codemod/pull/21) ([adamchainz](https://github.com/adamchainz))

## [v0.2.1](https://github.com/browniebroke/django-codemod/tree/v0.2.1) (2020-05-10)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.2.0...v0.2.1)

### 🚀 Enhancements:

- Migrate package metadata to declarative syntax [\#19](https://github.com/browniebroke/django-codemod/pull/19) ([browniebroke](https://github.com/browniebroke))

## [v0.2.0](https://github.com/browniebroke/django-codemod/tree/v0.2.0) (2020-05-10)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.1.1...v0.2.0)

### ⚠️ Breaking Changes:

- Rename commands to reflect the functions they work with [\#13](https://github.com/browniebroke/django-codemod/pull/13) ([browniebroke](https://github.com/browniebroke))
- Rename module and extract logic out into a base command [\#9](https://github.com/browniebroke/django-codemod/pull/9) ([browniebroke](https://github.com/browniebroke))

### 🚀 Enhancements:

- Support resolving django.utils.translation.ungettext\_lazy deprecation [\#17](https://github.com/browniebroke/django-codemod/pull/17) ([browniebroke](https://github.com/browniebroke))
- Support resolving django.utils.translation.ungettext deprecation [\#16](https://github.com/browniebroke/django-codemod/pull/16) ([browniebroke](https://github.com/browniebroke))
- Support resolving django.utils.translation.ugettext\_noop deprecation [\#15](https://github.com/browniebroke/django-codemod/pull/15) ([browniebroke](https://github.com/browniebroke))
- Support resolving django.utils.translation.ugettext\_lazy deprecation [\#14](https://github.com/browniebroke/django-codemod/pull/14) ([browniebroke](https://github.com/browniebroke))
- Support resolving django.utils.translation.ugettext deprecation [\#12](https://github.com/browniebroke/django-codemod/pull/12) ([browniebroke](https://github.com/browniebroke))
- Support smart\_text deprecation, replace by smart\_str [\#10](https://github.com/browniebroke/django-codemod/pull/10) ([browniebroke](https://github.com/browniebroke))
- Refactor checks to use matchers [\#8](https://github.com/browniebroke/django-codemod/pull/8) ([browniebroke](https://github.com/browniebroke))

### 🗑 Removals:

- Remove unused entry point [\#18](https://github.com/browniebroke/django-codemod/pull/18) ([browniebroke](https://github.com/browniebroke))

## [v0.1.1](https://github.com/browniebroke/django-codemod/tree/v0.1.1) (2020-05-07)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.1.0...v0.1.1)

## [v0.1.0](https://github.com/browniebroke/django-codemod/tree/v0.1.0) (2020-05-06)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/fc638d793736530009a48e5782c015ca5daafa86...v0.1.0)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
