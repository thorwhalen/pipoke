# pipoke.distribution

Tools to run on PyPi distribution of packages.

### Functions

| [`ensure_json_package_info`](#pipoke.distribution.ensure_json_package_info)(package_info)    | Gets and validates package info dicts from various sources.                     |
|--------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| [`format_str_vals_of_dict`](#pipoke.distribution.format_str_vals_of_dict)(d, \*[, ...])     | Traverse the values of a dict and apply string formatting to them, recursively. |
| [`get_version`](#pipoke.distribution.get_version)(package[, url_pattern])       | Return version of package on pypi.python.org using json.                        |
| `increment_version`(version_str)                                                           |                                                                                 |
| [`json_package_info`](#pipoke.distribution.json_package_info)(package[, url_pattern]) | Return version of package on pypi.python.org using json.                        |
| `last_release_date`(package)                                                               |                                                                                 |
| `my_setup`(\*\*setup_kwargs)                                                               |                                                                                 |
| [`package_info`](#pipoke.distribution.package_info)(package[, url_pattern])      | Return version of package on pypi.python.org using json.                        |
| `release_dates`(package)                                                                   |                                                                                 |
| `release_versions`(package)                                                                |                                                                                 |
| [`ujoin`](#pipoke.distribution.ujoin)(\*args)                             | Join strings with the url seperator (/).                                        |

### Classes

| [`PartialFormatter`](#pipoke.distribution.PartialFormatter)()   | A string formatter that won't complain if the fields are only partially formatted.   |
|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------|

### *class* pipoke.distribution.PartialFormatter

Bases: [`Formatter`](https://docs.python.org/3/library/string.html#string.Formatter)

A string formatter that won’t complain if the fields are only partially formatted.
But note that you will lose the spec part of your template (e.g. in {foo:1.2f},
you’ll loose the 1.2f if not foo is given – but {foo} will remain).

### pipoke.distribution.ensure_json_package_info(package_info)

Gets and validates package info dicts from various sources.

Namely, this is used in functions like `releases`, `release_dates` etc. so
that we can use them bother as fetcher+parser and as  parsers (giving them the
same info dict we already fetched, so we don’t have to fetch the info twice).

### pipoke.distribution.format_str_vals_of_dict(d, , max_formatting_loops=10, \*\*kwargs)

Traverse the values of a dict and apply string formatting to them, recursively.

* **Parameters:**
  * **d** – The template dict containing both format strings to be populated/embodied
    and (possibly) values to do so.
  * **max_formatting_loops** – The maximum number of loops.
  * **kwargs** – Extra values to use to populate string formats
* **Returns:**
  A (shallow) copy of the filled out (i.e. populated/embodied) dict

```pycon
>>> d = {
...     'filepath': '{root}/{file}.{ext}',
...     'ext': 'txt'
... }
>>> format_str_vals_of_dict(d, root='ROOT', file='FILE')
{'filepath': 'ROOT/FILE.txt', 'ext': 'txt'}
```

Note that if the input mapping `d` and the kwargs have a conflict, the mapping
version is used!

```pycon
>>> format_str_vals_of_dict(d, root='ROOT', file='FILE', ext='will_not_be_used')
{'filepath': 'ROOT/FILE.txt', 'ext': 'txt'}
```

But if you want to override an input mapping, you can – the usual way:

```pycon
>>> format_str_vals_of_dict(dict(d, ext='will_be_used'), root='ROOT', file='FILE')
{'filepath': 'ROOT/FILE.will_be_used', 'ext': 'will_be_used'}
```

If you don’t provide enough fields to satisfy all the format fields in the values
of `d`, you’ll be told to bugger off.

```pycon
>>> format_str_vals_of_dict(d, root='ROOT')
Traceback (most recent call last):
...
ValueError: I won't be able to complete that. You'll need to provide the values for:
  file
```

And it’s recursive…

```pycon
>>> d = {
...     'filepath': '{root}/{filename}',
...     'filename': '{file}.{ext}'
... }
>>> my_configs = {'root': 'ROOT', 'file': 'FILE', 'ext': 'EXT'}
>>> format_str_vals_of_dict(d, **my_configs)
{'filepath': 'ROOT/FILE.EXT', 'filename': 'FILE.EXT'}
```

# TODO: Could make the above work if filename is give, but not file nor ext!
#  At least as an option.

### pipoke.distribution.get_version(package, url_pattern='https://pypi.python.org/pypi/{package}/json')

Return version of package on pypi.python.org using json.

```pycon
>>> get_version('py2store')
'0.1.15'
```

### pipoke.distribution.json_package_info(package, url_pattern='https://pypi.python.org/pypi/{package}/json')

Return version of package on pypi.python.org using json.

Makes a real HTTPS request to PyPI, so this example is illustrative only
and is skipped by the doctest runner (pipoke#6): a PyPI outage or a
network-restricted CI runner must not fail the test suite. See
`pipoke.tests.test_distribution.test_json_package_info` for a
network-free, mocked equivalent.

```pycon
>>> d = json_package_info('ps')
>>> isinstance(d, dict)
True
>>> {'name', 'author', 'version'}.issubset(d['info'])
True
```

### pipoke.distribution.package_info(package, url_pattern='https://pypi.python.org/pypi/{package}/json')

Return version of package on pypi.python.org using json.

Makes a real HTTPS request to PyPI, so this example is illustrative only
and is skipped by the doctest runner (pipoke#6): a PyPI outage or a
network-restricted CI runner must not fail the test suite. See
`pipoke.tests.test_distribution.test_json_package_info` for a
network-free, mocked equivalent.

```pycon
>>> d = json_package_info('ps')
>>> isinstance(d, dict)
True
>>> {'name', 'author', 'version'}.issubset(d['info'])
True
```

### pipoke.distribution.ujoin(\*args)

Join strings with the url seperator (/).

Note that will add a / where it’s missing (as in between ‘[https://pypi.org](https://pypi.org)’ and ‘project/’),
and only use one if two consecutive tokens use respectively end and start with a /
(as in ‘project/’ and ‘/pipoke/’).

```pycon
>>> ujoin('https://pypi.org', 'project/', '/pipoke/')
'https://pypi.org/project/pipoke/'
```

Extremal cases

```pycon
>>> ujoin('https://pypi.org')
'https://pypi.org'
>>> ujoin('https://pypi.org/')
'https://pypi.org/'
>>> ujoin('')
''
>>> ujoin()
''
```
