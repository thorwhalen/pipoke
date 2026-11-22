# pipoke.misc

Miscellaneous helpers for relating python objects to modules and package names.

### Functions

| [`is_from_module`](#pipoke.misc.is_from_module)(obj, module)                 | Check if an object "belongs" to a module.                                             |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| [`multiple_word_vs_pkgs_regex_stats`](#pipoke.misc.multiple_word_vs_pkgs_regex_stats)(patterns) | Get proportions of english and pkg names that satisfy a regex pattern                 |
| [`second_party_names`](#pipoke.misc.second_party_names)(module[, obj_filt])      | Generator of module attribute names that point to object the module actually defines. |
| [`subsequence_counts`](#pipoke.misc.subsequence_counts)([n, n_of_top_counts])    | Get counts of subsequences of letters in english and pypi pkg words                   |
| `word_vs_pkgs_regex_stats`(regex)                                                            |                                                                                       |
| `words_containing_py_free_for_pkg`()                                                         |                                                                                       |
| `words_ending_with_py_free_for_pkg`()                                                        |                                                                                       |
| `words_starting_with_py_free_for_pkg`()                                                      |                                                                                       |

### pipoke.misc.is_from_module(obj, module)

Check if an object “belongs” to a module.

```pycon
>>> import collections
>>> is_from_module(collections.ChainMap, collections)
True
>>> is_from_module(is_from_module, collections)
False
```

### pipoke.misc.multiple_word_vs_pkgs_regex_stats(patterns)

Get proportions of english and pkg names that satisfy a regex pattern

* **Parameters:**
  **patterns**
* **Returns:**

### pipoke.misc.second_party_names(module, obj_filt=None)

Generator of module attribute names that point to object the module actually defines.

* **Parameters:**
  * **module** – Module (object)
  * **obj_filt** – Boolean function applied to object to filter it in
* **Returns:**

```pycon
>>> import collections
>>> names = sorted(second_party_names(collections))
>>> 'ChainMap' in names and 'OrderedDict' in names
True
```

Names the module merely imports are excluded:

```pycon
>>> 'abc' in names
False
```

`obj_filt` narrows the result further:

```pycon
>>> classes = sorted(second_party_names(collections, lambda o: isinstance(o, type)))
>>> 'Counter' in classes and 'namedtuple' not in classes
True
```

### pipoke.misc.subsequence_counts(n=2, n_of_top_counts=10)

Get counts of subsequences of letters in english and pypi pkg words

* **Parameters:**
  * **n**
  * **n_of_top_counts**
* **Returns:**
