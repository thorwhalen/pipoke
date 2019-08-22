# What's this?

Some tools to get data from pypi and kick it around, for fun and profit.

Minus the profit.

You can do stuff in python, but also have a CLI for most of the stuff. 

```bash
$ python pipoke/pkg_vs_words.py is-not-a-pkg-name "numpy,exists,but,this_crazy_pkg,does,not"
{'this_crazy_pkg', 'but', 'exists', 'does'}
```
So 'numpy' and 'not' are already registered with pypi. 
But hey, the good news is 'but' and 'does' aren't. 
Inspired to write some code bearing that name?
 
# Cool! How do I install it?

```bash
pip install pipoke
```

Enough said.

# Play

```python
from pipoke.pkg_vs_words import all_words, pkg_names
all_words  # set of all English words (according to wordnet)
pkg_names  # set of all PyPi package names. All at the point the list was slurped
```

You can have your own fun with that. Here are a few things to get you started. 

All pkg_names that are valid English words:
```python
from pipoke.pkg_vs_words import all_words, pkg_names
set(all_words).intersection(pkg_names)
```

All valid English words that are no "taken" by the pypi namespace:
```python
from pipoke.pkg_vs_words import all_words, pkg_names
set(all_words).difference(pkg_names)
```

All english words, package names, and intersection of both... that end with py:
```python
from pipoke.pkg_vs_words import words_and_pkg_names_satisfying_condition
words_and_pkg_names_satisfying_condition(lambda w: w.endswith('py'), print_counts=True)
```

All english words, package names, and intersection of both... that contain py or pi:
```python
from pipoke.pkg_vs_words import words_and_pkg_names_satisfying_condition
import pipoke.word_conditions as wc
words_and_pkg_names_satisfying_condition(wc.contains_py_or_pi, print_counts=True)
```

Want to search with a regular expression? Got you covered. 
The above search is actually equivalent to:
```python
from pipoke.pkg_vs_words import words_and_pkg_names_satisfying_regex
words_and_pkg_names_satisfying_regex('.*(py|pi).*', print_counts=True)
```

# Get stuff

The repository comes with a data folder that contains a pickle containing a set of words (from wordnet) 
and a set of pypi package names (well {pkg_name: pkg_url_stub, } to be exact). 

But you probably want to update that pypi list from time to time. And you can do so with

```python 
from pipoke.pypi_store import refresh_saved_pkg_name_stub
refresh_saved_pkg_name_stub()
```

Get dict of information for a pkg_name:

```python
from pipoke.pypi_store import info_of_pkg_from_web
pkg_name = 'pipoke'
info_of_pkg_from_web(pkg_name)
```

# And by the way

You have a CLI for many of these things too.