# django-modeltrans change log

## 0.1.1 (2017-10-23)
 - Allow adding `MultilingualManager()` as a manager to objects without translations to allow lookups
   of translated content through those managers.

## 0.1.0 (2017-10-23)
 - Use proper alias in subqueries, fixes #23.
 - Support lookups on and ordering by related translated fields (`.filter(category__name_nl='Vogels')`), fixes #13.
 - Use `KeyTextTransform()` rather than `RawSQL()` to access keys in the `JSONField`. For Django 1.9 and 1.10 the Django 1.11 version is used.

## 0.0.8 (2017-10-19)
 - Check if `MODELTRANS_AVAILABLE_LANGUAGES` only contains strings.
 - Make sure `settings.LANGUAGE_CODE` is never returned from `conf.get_available_languages()`

## 0.0.7 (2017-09-04)
 - Cleaned up the settings used by django-modeltrans [#19](https://github.com/zostera/django-modeltrans/pull/19).
   This might be a breaking change, depending on your configuration.
    * `AVAILABLE_LANGUAGES` is now renamed to `MODELTRANS_AVAILABLE_LANGUAGES` and defaults to the language codes in the
      django `LANGUAGES` setting.
    * `DEFAULT_LANGUAGE` is removed, instead, django-modeltrans uses the django `LANGUAGE_CODE` setting.
 - Added per-language configurable fallback using the `MODELTRANS_FALLBACK` setting.

## 0.0.6 (2017-08-29)
 - Also fall back to `DEFAULT_LANGUAGE` if the value for a key in the translations dict is falsy.

## 0.0.5 (2017-07-26)
 - Removed registration in favour of adding the `TranslationField` to a model you need to translated.
 - Created documentation.

## 0.0.4 (2017-05-19)
 - Improve robustness of rewriting lookups in QuerySets

## 0.0.3 (2017-05-18)
 - Add the `gin` index in the data migration.
 - Added tests for the migration procedure.
