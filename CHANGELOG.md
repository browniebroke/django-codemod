# Changelog

<!--next-version-placeholder-->

## v1.4.1 (2021-04-02)
### Fix
* Update type annotations ([`24f9093`](https://github.com/browniebroke/django-codemod/commit/24f9093673cc7241e77966d9cdbeca12b8f7b4f2))
* **deps:** Update dependency libcst to <=0.3.18 ([`ca35714`](https://github.com/browniebroke/django-codemod/commit/ca35714da223c43e275061a0117f2769b974bc12))
* **deps:** Update dependency rich to v10 ([`3841299`](https://github.com/browniebroke/django-codemod/commit/3841299fae4807edba97f2876a91ba9363f38d39))

## v1.4.0 (2021-03-02)
### Feature
* Handle rename when parent module is imported ([#347](https://github.com/browniebroke/django-codemod/issues/347)) ([`26d22fe`](https://github.com/browniebroke/django-codemod/commit/26d22fef90654c8e730e302e7bdef1f4d2a9530c))

## v1.3.7 (2021-02-09)
### Fix
* **deps:** Update dependency libcst to <=0.3.17 ([`76dbc7c`](https://github.com/browniebroke/django-codemod/commit/76dbc7c7e0ccdd53fcd6263ee527f23d24bb55a6))

## v1.3.6 (2021-02-02)
### Fix
* Mypy issues when following imports ([#328](https://github.com/browniebroke/django-codemod/issues/328)) ([`4fb45f8`](https://github.com/browniebroke/django-codemod/commit/4fb45f83265ff8e77e62b157a110915defe49bf0))
* Type hint issues ([`b11a68c`](https://github.com/browniebroke/django-codemod/commit/b11a68c47912b3a87593b24d58302003c01d6c77))
* Error with star import ([`56d09b7`](https://github.com/browniebroke/django-codemod/commit/56d09b7d56cf757ac3d1e9fcdd3a083f167554b5))

### Documentation
* Add logo ([`82d1419`](https://github.com/browniebroke/django-codemod/commit/82d1419e1b00e439f9ca2bb2e04f3079700d458f))

## v1.3.5 (2021-01-27)
### Fix
* Loosen up version for libcst ([`4129e23`](https://github.com/browniebroke/django-codemod/commit/4129e2372f1deae58c68a2d4e5a202576170299e))

## v1.3.4 (2021-01-21)
### Fix
* Don't confuse kwargs with symbol to codemod ([`f576347`](https://github.com/browniebroke/django-codemod/commit/f576347a4e387a7e478142e29a1a3e189ee38cd9))

## v1.3.3 (2021-01-21)
### Fix
* Bug with attributes accessing ([`417e630`](https://github.com/browniebroke/django-codemod/commit/417e6302ed6c3182fba2199888610c19f35c5105))
* Bug with scopes ([`3dcee1d`](https://github.com/browniebroke/django-codemod/commit/3dcee1db59a8e5c14d54537872e4c95d0320fa18))
* Add some missing type hints ([`a403e90`](https://github.com/browniebroke/django-codemod/commit/a403e906d3cb14d99cd6880964c1a3ed54e0b9db))

## v1.3.2 (2021-01-19)
### Fix
* Bug when `url()` route uses the `regex` kwarg ([`b7bcc3d`](https://github.com/browniebroke/django-codemod/commit/b7bcc3dee08fadc90afdc9490828569e7ec06786))

## v1.3.1 (2021-01-19)
### Fix
* Pin libCST to 0.3.13 ([`8269370`](https://github.com/browniebroke/django-codemod/commit/8269370d4e6e4d40c3e706b7e8b0008ea3cd0e85))
* Support another slug pattern ([`a4ce0cb`](https://github.com/browniebroke/django-codemod/commit/a4ce0cb039a24ebee86d7ff0cabe620ff0ab3f3c))
* Migrate partial patterns to path ([`202a6b3`](https://github.com/browniebroke/django-codemod/commit/202a6b3cde651173d91386d01ad5399e106049f3))

## v1.3.0 (2021-01-14)
### Feature
* Add fixer for `django.utils.http.cookie_date` ([`a3e12d1`](https://github.com/browniebroke/django-codemod/commit/a3e12d1c867345133c8bf77c30085edb41f1e800))

### Documentation
* Add @drewbrew as a contributor ([`08ed73b`](https://github.com/browniebroke/django-codemod/commit/08ed73ba97c1525ff047668923761d02e9150ed0))
* Explain limitation with gitignore ([`e102bde`](https://github.com/browniebroke/django-codemod/commit/e102bde122a562a4b20f3a7977895bfc0a663202))

## v1.2.0 (2021-01-05)
### Feature
* Make it runnable as pre-commit hook ([#294](https://github.com/browniebroke/django-codemod/issues/294)) ([`2f78502`](https://github.com/browniebroke/django-codemod/commit/2f78502a9755436e2d4b7aa54a8a52c6acc27c77))

### Fix
* Add pathspec to dependencies ([`2cb8a82`](https://github.com/browniebroke/django-codemod/commit/2cb8a82f53d307ded2f878b83ea5de0cb5aa0677))

## v1.1.0 (2021-01-02)
### Feature
* Ignore files according to .gitignore ([`ae74273`](https://github.com/browniebroke/django-codemod/commit/ae742731fc91c7d130b6fc5c6ab91bac92299151))

### Fix
* **deps:** Update dependency myst-parser to ^0.13.0 ([`c9ac21a`](https://github.com/browniebroke/django-codemod/commit/c9ac21a570149bec2ae6673e0cfba37104e35bb4))
* **deps:** Update dependency rich to v9 ([`6818668`](https://github.com/browniebroke/django-codemod/commit/68186681a9791734fb0e40471446a7ad7a37a6e0))

### Documentation
* Rework documentation ([`5e9dc2b`](https://github.com/browniebroke/django-codemod/commit/5e9dc2b1723fa110bd01954fc2e198ca23533dc9))
* Make recommended command less error prone ([`fc51862`](https://github.com/browniebroke/django-codemod/commit/fc51862417d3ae42e9006e460ebdc9b6cbeefc30))

## v1.0.0 (2020-11-11)
### Feature
* Migrate packaging to Poetry ([`8ed12c8`](https://github.com/browniebroke/django-codemod/commit/8ed12c898c8a8eb63b3e9b005e20af635bf8cc42))

### Breaking
* Stable release  ([`8ed12c8`](https://github.com/browniebroke/django-codemod/commit/8ed12c898c8a8eb63b3e9b005e20af635bf8cc42))

## v0.21.0 (2020-10-19)
### Feature
* Cli: add --codemod option ([`0ffe315`](https://github.com/browniebroke/django-codemod/commit/0ffe315fc0201d16360afea9cb8bf6c8efcc76fc))
* Add codemod to add a length parameter to get_random_string() ([`f88f56d`](https://github.com/browniebroke/django-codemod/commit/f88f56de5f9b6de4f9bec13fdb80530f38d60db5))
* Add find_keyword_arg utility ([`111dd37`](https://github.com/browniebroke/django-codemod/commit/111dd37ed781a5dfbdb4ba7e2c7f50d5d94d90a9))
* Add a transformer for the new core JSONField in Django 3.1 ([`7ca1c99`](https://github.com/browniebroke/django-codemod/commit/7ca1c999c26ab3b2752d3542dc9a37c8a2f25f4f))

### Fix
* Avoid changing import list if old name is new name ([`c3fecb3`](https://github.com/browniebroke/django-codemod/commit/c3fecb32a4f8e0a484fb52349f2710f2df4c7a9a))
* Allow both removed-in and deprecated-in as well as multiple arguments for both ([`d89676b`](https://github.com/browniebroke/django-codemod/commit/d89676b236da1c21c716709deb8a766a93a76eb2))
* Sort valid versions semantically ([`ab4c20e`](https://github.com/browniebroke/django-codemod/commit/ab4c20eeae7c3edb2c116da08836d44af340413f))

## v0.20.0 (2020-10-13)
### Feature
* CLI: Support multiple target `path` arguments ([`8dafb0f`](https://github.com/browniebroke/django-codemod/commit/8dafb0faff7e9681a5a80341830d9d674804636e))
* URLs: allow `path()` instead of `re_path()` if a path contains dashes ([`de744cf`](https://github.com/browniebroke/django-codemod/commit/de744cfb24f931ed3f9c8e9b4fd72e699d9730b9))

## v0.19.0 (2020-10-10)
### Feature
* Add support for Python 3.9 ([`904ba55`](https://github.com/browniebroke/django-codemod/commit/904ba5565efef38c46c3d2ed65edf694fcc1760e))

### Documentation
* Add iamshnoo as a contributor (#221) ([`4758bd6`](https://github.com/browniebroke/django-codemod/commit/4758bd6725a44d174c9d5ae65182acc5853a770d))

## v0.18.0 (2020-09-21)
### Feature
* Remove the weak argument from Signal.disconnect() ([`ab41491`](https://github.com/browniebroke/django-codemod/commit/ab414910e3e1fa1b04af9dd200d0a07cbe65c3f3))
* Add a transformer for assignment_tag ([`cb8afdd`](https://github.com/browniebroke/django-codemod/commit/cb8afddab1249ae3126eabdb7002ea1df6e724d3))

## v0.17.5 (2020-09-17)
### Fix
* More version bump to test deployment ([`ece3df2`](https://github.com/browniebroke/django-codemod/commit/ece3df2e10aeeb3de3b134623b53aeda01df1786))

## v0.17.4 (2020-09-17)
### Fix
* No actual changes, version bump to test deployment ([d0824c2](https://github.com/browniebroke/django-codemod/commit/d0824c2c09a4634d0afa7d3719ab660c95399b6e))

## v0.17.3 (2020-09-17)
### Fix
* No actual changes, version bump to test deployment ([b57aedfc4a77c6c6f6d951dc071a5b2ebf8cd951](https://github.com/browniebroke/django-codemod/commit/b57aedfc4a77c6c6f6d951dc071a5b2ebf8cd951))

## v0.17.2 (2020-09-17)
### Fix
* No actual changes, version bump to test deployment (10e16e34dea4762af94fd911434307e505580a38)

### Documentation
* Update changelog (98734602da59edbf485d87123902414981f5e952)

## [v0.17.1](https://github.com/browniebroke/django-codemod/tree/v0.17.1) (2020-09-17)

- No actual changes, just a minor version bump to test new deployment.

## [v0.17.0](https://github.com/browniebroke/django-codemod/tree/v0.17.0) (2020-09-16)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.16.0...v0.17.0)

### 🚀 Enhancements:

- Add commitlint to pre-commit hooks config [\#200](https://github.com/browniebroke/django-codemod/pull/200) ([browniebroke](https://github.com/browniebroke))
- Add transformer for `request.xreadlines\(\)` [\#199](https://github.com/browniebroke/django-codemod/pull/199) ([browniebroke](https://github.com/browniebroke))

## [v0.16.0](https://github.com/browniebroke/django-codemod/tree/v0.16.0) (2020-09-15)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.15.0...v0.16.0)

### 🚀 Enhancements:

- Add visitor to replace usages of postgres' `FloatRangeFormField` [\#198](https://github.com/browniebroke/django-codemod/pull/198) ([browniebroke](https://github.com/browniebroke))

## [v0.15.0](https://github.com/browniebroke/django-codemod/tree/v0.15.0) (2020-09-15)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.14.0...v0.15.0)

### 🚀 Enhancements:

- New visitor to replace usages of `QuerySetPaginator` [\#196](https://github.com/browniebroke/django-codemod/pull/196) ([browniebroke](https://github.com/browniebroke))

### 🐛 Bug Fixes:

- Fix support renaming of usages of function without calls [\#197](https://github.com/browniebroke/django-codemod/pull/197) ([browniebroke](https://github.com/browniebroke))

### ✅ Testing:

- Internal refactoring of CLI and test improvements [\#157](https://github.com/browniebroke/django-codemod/pull/157) ([browniebroke](https://github.com/browniebroke))

## [v0.14.0](https://github.com/browniebroke/django-codemod/tree/v0.14.0) (2020-09-15)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.13.3...v0.14.0)

### 🚀 Enhancements:

- New visitor to replace `timezone.FixedOffset` by `datetime.timezone` [\#194](https://github.com/browniebroke/django-codemod/pull/194) ([browniebroke](https://github.com/browniebroke))

## [v0.13.3](https://github.com/browniebroke/django-codemod/tree/v0.13.3) (2020-09-15)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.13.2...v0.13.3)

## [v0.13.2](https://github.com/browniebroke/django-codemod/tree/v0.13.2) (2020-09-15)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.13.1...v0.13.2)

### ✅ Testing:

- Use semantic release to publish [\#195](https://github.com/browniebroke/django-codemod/pull/195) ([browniebroke](https://github.com/browniebroke))

## [v0.13.1](https://github.com/browniebroke/django-codemod/tree/v0.13.1) (2020-09-14)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.13.0...v0.13.1)

### 🐛 Bug Fixes:

- fix\(packaging\): Python wheels are not for Python 2 [\#193](https://github.com/browniebroke/django-codemod/pull/193) ([browniebroke](https://github.com/browniebroke))

## [v0.13.0](https://github.com/browniebroke/django-codemod/tree/v0.13.0) (2020-07-26)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.12.0...v0.13.0)

### 🚀 Enhancements:

- Add CLI command to list all codemodders [\#156](https://github.com/browniebroke/django-codemod/pull/156) ([browniebroke](https://github.com/browniebroke))

## [v0.12.0](https://github.com/browniebroke/django-codemod/tree/v0.12.0) (2020-07-21)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.11.0...v0.12.0)

### 🚀 Enhancements:

- Support replacing call to `url` with simple patterns by `path` [\#138](https://github.com/browniebroke/django-codemod/pull/138) ([browniebroke](https://github.com/browniebroke))

## [v0.11.0](https://github.com/browniebroke/django-codemod/tree/v0.11.0) (2020-07-20)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.10.1...v0.11.0)

### 🚀 Enhancements:

- Add module rename support and URLResolversTransformer [\#123](https://github.com/browniebroke/django-codemod/pull/123) ([jayvdb](https://github.com/jayvdb))

## [v0.10.1](https://github.com/browniebroke/django-codemod/tree/v0.10.1) (2020-07-17)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.10.0...v0.10.1)

### 🚀 Enhancements:

- Rename constants for numerical sorting [\#139](https://github.com/browniebroke/django-codemod/pull/139) ([jayvdb](https://github.com/jayvdb))

### ✅ Testing:

- Split tests and docs requirements [\#131](https://github.com/browniebroke/django-codemod/pull/131) ([browniebroke](https://github.com/browniebroke))
- Upload coverage report using codecov action [\#130](https://github.com/browniebroke/django-codemod/pull/130) ([browniebroke](https://github.com/browniebroke))

## [v0.10.0](https://github.com/browniebroke/django-codemod/tree/v0.10.0) (2020-07-04)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.9.0...v0.10.0)

### 🚀 Enhancements:

- Add support for adding `on\_delete` for `ForeignKey` and `OneToOneField` [\#117](https://github.com/browniebroke/django-codemod/pull/117) ([cvanderkolk](https://github.com/cvanderkolk))

### 🐛 Bug Fixes:

- Fix bug with CLI processing entire filesystem [\#126](https://github.com/browniebroke/django-codemod/pull/126) ([browniebroke](https://github.com/browniebroke))

### ✅ Testing:

- Move CODECOV\_TOKEN from cmd line option to environment [\#118](https://github.com/browniebroke/django-codemod/pull/118) ([browniebroke](https://github.com/browniebroke))

## [v0.9.0](https://github.com/browniebroke/django-codemod/tree/v0.9.0) (2020-06-18)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0...v0.9.0)

## [v0](https://github.com/browniebroke/django-codemod/tree/v0) (2020-06-18)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.8.1...v0)

### 🚀 Enhancements:

- Handle deprecation of `@models.permalink` decorator in Django 1.11 [\#87](https://github.com/browniebroke/django-codemod/pull/87) ([browniebroke](https://github.com/browniebroke))
- Resolve deprecation of `django.utils.decorators.available\_attrs` in Django 2.0 [\#85](https://github.com/browniebroke/django-codemod/pull/85) ([browniebroke](https://github.com/browniebroke))
- Resolve deprecation of `django.utils.decorators.ContextDecorator` in Django 2.0 [\#84](https://github.com/browniebroke/django-codemod/pull/84) ([browniebroke](https://github.com/browniebroke))

### 🔥 Removals:

- Remove the custom hardcoded libCST commands [\#114](https://github.com/browniebroke/django-codemod/pull/114) ([browniebroke](https://github.com/browniebroke))

### 📖 Documentation updates:

- Convert documentation to Markdown using MyST parser [\#113](https://github.com/browniebroke/django-codemod/pull/113) ([browniebroke](https://github.com/browniebroke))

### ✅ Testing:

- Use codecov to upload coverage data cross-platform [\#105](https://github.com/browniebroke/django-codemod/pull/105) ([browniebroke](https://github.com/browniebroke))
- Remove Travis CI [\#103](https://github.com/browniebroke/django-codemod/pull/103) ([browniebroke](https://github.com/browniebroke))

## [v0.8.1](https://github.com/browniebroke/django-codemod/tree/v0.8.1) (2020-06-07)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.8.0...v0.8.1)

### 🐛 Bug Fixes:

- Support fixing calls to base class `has\_add\_permission` in `AdminInline` [\#83](https://github.com/browniebroke/django-codemod/pull/83) ([browniebroke](https://github.com/browniebroke))

### 📖 Documentation updates:

- Mention changes around tests in changelog [\#82](https://github.com/browniebroke/django-codemod/pull/82) ([browniebroke](https://github.com/browniebroke))

### ✅ Testing:

- Increase test code coverage to 100% [\#81](https://github.com/browniebroke/django-codemod/pull/81) ([browniebroke](https://github.com/browniebroke))

## [v0.8.0](https://github.com/browniebroke/django-codemod/tree/v0.8.0) (2020-06-02)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.7.0...v0.8.0)

### 🚀 Enhancements:

- Resolve some removed private Python 2 compatibility APIs [\#74](https://github.com/browniebroke/django-codemod/pull/74) ([browniebroke](https://github.com/browniebroke))
- Resolve deprecation of `django.utils.http.is\_safe\_url` in Django 3.0 [\#72](https://github.com/browniebroke/django-codemod/pull/72) ([browniebroke](https://github.com/browniebroke))
- Resolve deprecation of `django.utils.text.unescape\_entities` in Django 3.0 [\#70](https://github.com/browniebroke/django-codemod/pull/70) ([browniebroke](https://github.com/browniebroke))
- Resolve deprecations from `django.utils.http` in Django 3.0 [\#69](https://github.com/browniebroke/django-codemod/pull/69) ([browniebroke](https://github.com/browniebroke))
- Add new CLI option `--deprecated-in` [\#64](https://github.com/browniebroke/django-codemod/pull/64) ([browniebroke](https://github.com/browniebroke))
- Make `InlineHasAddPermissionsTransformer` more robust [\#60](https://github.com/browniebroke/django-codemod/pull/60) ([browniebroke](https://github.com/browniebroke))

### 🐛 Bug Fixes:

- Fix version deprecated for several Django 4.0 visitors [\#68](https://github.com/browniebroke/django-codemod/pull/68) ([browniebroke](https://github.com/browniebroke))

### ✅ Testing:

- Test that transformers are found by CLI [\#71](https://github.com/browniebroke/django-codemod/pull/71) ([browniebroke](https://github.com/browniebroke))

## [v0.7.0](https://github.com/browniebroke/django-codemod/tree/v0.7.0) (2020-05-23)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.6.0...v0.7.0)

### 🚀 Enhancements:

- Add a `djcodemod` CLI [\#55](https://github.com/browniebroke/django-codemod/pull/55) ([browniebroke](https://github.com/browniebroke))

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

### 🔥 Removals:

- Remove commands to fix single deprecations [\#43](https://github.com/browniebroke/django-codemod/pull/43) ([browniebroke](https://github.com/browniebroke))

### ✅ Testing:

- Linting workflow [\#47](https://github.com/browniebroke/django-codemod/pull/47) ([browniebroke](https://github.com/browniebroke))
- Tests visitors independently from commands [\#42](https://github.com/browniebroke/django-codemod/pull/42) ([browniebroke](https://github.com/browniebroke))

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

### 💥 Breaking Changes:

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

### 🔥 Removals:

- Remove unused entry point [\#18](https://github.com/browniebroke/django-codemod/pull/18) ([browniebroke](https://github.com/browniebroke))

## [v0.1.1](https://github.com/browniebroke/django-codemod/tree/v0.1.1) (2020-05-07)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/v0.1.0...v0.1.1)

## [v0.1.0](https://github.com/browniebroke/django-codemod/tree/v0.1.0) (2020-05-06)

[Full Changelog](https://github.com/browniebroke/django-codemod/compare/fc638d793736530009a48e5782c015ca5daafa86...v0.1.0)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
