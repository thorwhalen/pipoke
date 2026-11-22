# pipoke.pkg_vs_words

Compare package names with words (e.g. which package names are also dictionary words).

### Functions

| `disp_str_for_counts`(words, pkgs, pkgs_words)                                               |                                                                                             |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `get_all_words_from_wordnet`()                                                               |                                                                                             |
| [`is_not_a_pkg_name`](#pipoke.pkg_vs_words.is_not_a_pkg_name)([regex, words])           | Filter words, keeping only those that are not already pypi package names.                   |
| `is_standard_lib_path`(path)                                                                 |                                                                                             |
| `standard_lib_module_names`([...])                                                           |                                                                                             |
| `str_for_func`(func)                                                                         |                                                                                             |
| `words_and_pkg_names_satisfying_condition`(cond)                                             |                                                                                             |
| [`words_and_pkg_names_satisfying_regex`](#pipoke.pkg_vs_words.words_and_pkg_names_satisfying_regex)(regex) | Get (English) words, pypi package names, and strings that are both words and package names. |

### pipoke.pkg_vs_words.is_not_a_pkg_name(regex='.\*', words=None)

Filter words, keeping only those that are not already pypi package names.

* **Parameters:**
  * **regex** – Extra (regular expression) filter to apply
  * **words** – The words you want to filter. By default will take all (simple) words of the (wordnet) dictionary.
* **Returns:**
  The subset of input words that are not pypi package names

### pipoke.pkg_vs_words.words_and_pkg_names_satisfying_regex(regex, print_counts=False)

Get (English) words, pypi package names, and strings that are both words and package names.

* **Parameters:**
  * **regex** – Regular expression that should match the WHOLE string
  * **print_counts** – Print count statistics
* **Returns:**
