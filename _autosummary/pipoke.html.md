# pipoke

pipoke

### Functions

| `words_and_pkg_names_satisfying_condition`(cond)                                             |                                                                                                 |
|----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| [`words_and_pkg_names_satisfying_regex`](#pipoke.words_and_pkg_names_satisfying_regex)(regex) | Get (English) words, pypi package names, and strings that are both words and package names.     |
| [`is_not_a_pkg_name`](#pipoke.is_not_a_pkg_name)([regex, words])           | Filter words, keeping only those that are not already pypi package names.                       |
| [`refresh_saved_pkg_name_stub`](#pipoke.refresh_saved_pkg_name_stub)([verbose, ...]) | Update the `{pkg_name: pkg_stub}` stored data with a fresh call to `get_updated_pkg_name_stub`. |
| [`info_of_pkg_from_web`](#pipoke.info_of_pkg_from_web)(pkg_name)              | Get dict of information for a pkg_name                                                          |
| [`get_version`](#pipoke.get_version)(package[, url_pattern])         | Return version of package on pypi.python.org using json.                                        |

### pipoke.get_version(package, url_pattern='https://pypi.python.org/pypi/{package}/json')

Return version of package on pypi.python.org using json.

```pycon
>>> get_version('py2store')
'0.1.15'
```

### pipoke.info_of_pkg_from_web(pkg_name)

Get dict of information for a pkg_name

* **Parameters:**
  **pkg_name**
* **Returns:**

### pipoke.is_not_a_pkg_name(regex='.\*', words=None)

Filter words, keeping only those that are not already pypi package names.

* **Parameters:**
  * **regex** – Extra (regular expression) filter to apply
  * **words** – The words you want to filter. By default will take all (simple) words of the (wordnet) dictionary.
* **Returns:**
  The subset of input words that are not pypi package names

### pipoke.refresh_saved_pkg_name_stub(verbose=True, , save_to=None, write_text_file=True)

Update the `{pkg_name: pkg_stub}` stored data with a fresh call to
`get_updated_pkg_name_stub`.

The refreshed copy is written to the user’s app folder by default, not into the
installed package, which is read-only in many installs.

* **Parameters:**
  * **save_to** – Where to write the gzipped TSV cache.
    Defaults to `pkg_names_user_filepath`.
  * **write_text_file** – Also write a plain `pkg_list.txt` of the names, one per
    line, alongside `save_to`.

### pipoke.words_and_pkg_names_satisfying_regex(regex, print_counts=False)

Get (English) words, pypi package names, and strings that are both words and package names.

* **Parameters:**
  * **regex** – Regular expression that should match the WHOLE string
  * **print_counts** – Print count statistics
* **Returns:**

### Modules

| [`distribution`](pipoke.distribution.html.md#module-pipoke.distribution)       | Tools to run on PyPi distribution of packages.                                                                            |
|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| [`misc`](pipoke.misc.html.md#module-pipoke.misc)                       | Miscellaneous helpers for relating python objects to modules and package names.                                           |
| [`pkg_diagnosis`](pipoke.pkg_diagnosis.html.md#module-pipoke.pkg_diagnosis)     | Pip installed package diagnosis The tools here will help you install and diagnose packages in a test virtual environment. |
| [`pkg_vs_words`](pipoke.pkg_vs_words.html.md#module-pipoke.pkg_vs_words)       | Compare package names with words (e.g. which package names are also dictionary words).                                    |
| [`pypi_store`](pipoke.pypi_store.html.md#module-pipoke.pypi_store)           | A mapping view to pypi projects Is now maintained in the `https://pypi.org/project/yp/` project.                          |
| [`word_conditions`](pipoke.word_conditions.html.md#module-pipoke.word_conditions) | Small predicates on words, used to characterize package names.                                                            |
