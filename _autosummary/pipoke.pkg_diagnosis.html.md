# pipoke.pkg_diagnosis

Pip installed package diagnosis
The tools here will help you install and diagnose packages in a test virtual
environment.

Here, checkout diagnose_pkgs, which takes a list of packages and runs a list of
diagnoses on each package, returning a dictionary of the results.
This functionality is also available from the command line using the script
diagnose_pkgs.py (or the shell script diagnose-pkgs).

### Functions

| [`activate_virtualenv`](#pipoke.pkg_diagnosis.activate_virtualenv)(virtualenv_path)              | Activate a virtual environment given its path.                                                                   |
|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [`activate_virtualenv_with_pyenv`](#pipoke.pkg_diagnosis.activate_virtualenv_with_pyenv)(...)               | Activate a virtual environment using pyenv given its name.                                                       |
| [`create_virtualenv`](#pipoke.pkg_diagnosis.create_virtualenv)([virtual_env, ...])             | Create a virtual environment using specified managers if it doesn't exist.                                       |
| [`create_virtualenv_with_pyenv`](#pipoke.pkg_diagnosis.create_virtualenv_with_pyenv)(...)                 | Create a virtual environment using pyenv if it doesn't exist.                                                    |
| [`current_virtual_environment_path`](#pipoke.pkg_diagnosis.current_virtual_environment_path)()                | Returns the path of the current virtual environment the function is called from                                  |
| `dflt_folder_diagnosis`(pkg_folder)                                                                |                                                                                                                  |
| `dflt_json_info_extractor`(pkg_name)                                                               |                                                                                                                  |
| `dflt_pkg_diagnosis`(imported_pkg)                                                                 |                                                                                                                  |
| [`diagnose_pkg`](#pipoke.pkg_diagnosis.diagnose_pkg)(pkg_name[, diagnoses, ...])          | Diagnose a package, given it's name                                                                              |
| [`diagnose_pkgs`](#pipoke.pkg_diagnosis.diagnose_pkgs)(pkgs[, diagnoses, ...])             | Diagnose a list of packages                                                                                      |
| `fullpath`(path)                                                                                   |                                                                                                                  |
| [`generate_diagnoses`](#pipoke.pkg_diagnosis.generate_diagnoses)(pkg_name[, diagnoses, ...])    | Runs through the diagnoses and yields the results.                                                               |
| [`get_pyenv_virtualenv_path`](#pipoke.pkg_diagnosis.get_pyenv_virtualenv_path)(...)                    | Get the path of a virtual environment managed by pyenv given its name.                                           |
| [`install_package`](#pipoke.pkg_diagnosis.install_package)(pkg_name[, virtual_env, verbose]) | Install a package in the virtual environment if not already installed.                                           |
| [`is_package_installed`](#pipoke.pkg_diagnosis.is_package_installed)(pkg_name)                    | Check if a package is installed in the virtual environment.                                                      |
| [`json_package_info`](#pipoke.pkg_diagnosis.json_package_info)(package[, url_pattern])         | Return version of package on pypi.python.org using json.                                                         |
| `main`()                                                                                           |                                                                                                                  |
| `manage_installation`(pkg_name[, ...])                                                             |                                                                                                                  |
| [`pyenv_exists`](#pipoke.pkg_diagnosis.pyenv_exists)()                                    | Check if pyenv is installed.                                                                                     |
| [`run_folder_diagnosis`](#pipoke.pkg_diagnosis.run_folder_diagnosis)(pkg_name[, ...])             | Run a diagnosis function on the folder containing the package's code folder.                                     |
| [`run_pkg_diagnosis`](#pipoke.pkg_diagnosis.run_pkg_diagnosis)(pkg_name[, pkg_diagnosis])      | Run a diagnosis function on the imported package.                                                                |
| [`run_pkg_tests`](#pipoke.pkg_diagnosis.run_pkg_tests)(pkg_name[, virtual_env])            | Run tests (including doctests, unittest tests, and pytest tests) for the installed package.                      |
| `venv_virtualenv_exists`(virtual_env)                                                              |                                                                                                                  |
| [`virtualenv_manager`](#pipoke.pkg_diagnosis.virtualenv_manager)(virtual_env[, ...])            | Check if a virtual environment was created using a specific manager, returning the name of the manager if found. |
| [`virtualenv_path`](#pipoke.pkg_diagnosis.virtualenv_path)(virtual_env[, virtual_envs_dir])  | Get the path of a virtual environment given its name.                                                            |

### Classes

| [`Settable`](#pipoke.pkg_diagnosis.Settable)(\*args, \*\*kwargs)   | A protocol for objects obj that support obj[k] = v   |
|---------------------------------------------------------------------------------|------------------------------------------------------|

### *class* pipoke.pkg_diagnosis.Settable(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

A protocol for objects obj that support obj[k] = v

### pipoke.pkg_diagnosis.activate_virtualenv(virtualenv_path)

Activate a virtual environment given its path.

### pipoke.pkg_diagnosis.activate_virtualenv_with_pyenv(virtual_environment_name)

Activate a virtual environment using pyenv given its name.

### pipoke.pkg_diagnosis.create_virtualenv(virtual_env=None, virtual_envs_dir='')

Create a virtual environment using specified managers if it doesn’t exist.

* **Parameters:**
  **virtual_env** – The path to the virtual environment
  :return True if the virtual environment exists or was created successfully, False otherwise

### pipoke.pkg_diagnosis.create_virtualenv_with_pyenv(virtual_environment_name)

Create a virtual environment using pyenv if it doesn’t exist.

* **Parameters:**
  **virtual_environment_name** – The name of the virtual environment
  :return True if the virtual environment exists or was created successfully, False otherwise

### pipoke.pkg_diagnosis.current_virtual_environment_path()

Returns the path of the current virtual environment the function is called from

### pipoke.pkg_diagnosis.diagnose_pkg(pkg_name, diagnoses=(('json_info', <function dflt_json_info_extractor>), ('pkg_diagnosis_result', <function run_pkg_diagnosis>), ('pkg_folder_diagnosis_result', <function run_folder_diagnosis>), ('test_diagnosis_result', <function run_pkg_tests>)), \*, install_pkg_if_not_installed=True, error_logger=<built-in function print>, verbose=True)

Diagnose a package, given it’s name

* **Parameters:**
  * **pkg_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The name of the package to diagnose
  * **diagnoses** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`object`](https://docs.python.org/3/builtins/functions.html#object)]]], [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`object`](https://docs.python.org/3/builtins/functions.html#object)]]) – A dictionary of diagnoses (name and function pairs)
  * **install_pkg_if_not_installed** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to install the package if it’s not installed
  * **error_logger** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)) – A function to log errors

### pipoke.pkg_diagnosis.diagnose_pkgs(pkgs, diagnoses=(('json_info', <function dflt_json_info_extractor>), ('pkg_diagnosis_result', <function run_pkg_diagnosis>), ('pkg_folder_diagnosis_result', <function run_folder_diagnosis>), ('test_diagnosis_result', <function run_pkg_tests>)), store_factory=<class 'dict'>, \*, install_pkg_if_not_installed=True, error_logger=<built-in function print>, verbose=True)

Diagnose a list of packages

* **Parameters:**
  * **pkgs** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – A list of packages to diagnose (or a filepath to a requirements file)
  * **diagnoses** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`object`](https://docs.python.org/3/builtins/functions.html#object)]]], [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`object`](https://docs.python.org/3/builtins/functions.html#object)], [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – What diagnoses to run
    (dict, (name, func) pairs, or requirements file)
  * **store_factory** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[], [`Settable`](#pipoke.pkg_diagnosis.Settable)]) – A factory that makes a store to store the results.
    If an (existing) folder path, will be stored in json files under that folder

### pipoke.pkg_diagnosis.generate_diagnoses(pkg_name, diagnoses=(('json_info', <function dflt_json_info_extractor>), ('pkg_diagnosis_result', <function run_pkg_diagnosis>), ('pkg_folder_diagnosis_result', <function run_folder_diagnosis>), ('test_diagnosis_result', <function run_pkg_tests>)), \*, error_logger=<built-in function print>)

Runs through the diagnoses and yields the results.

* **Parameters:**
  * **diagnoses** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)], [`object`](https://docs.python.org/3/builtins/functions.html#object)]]], [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`object`](https://docs.python.org/3/builtins/functions.html#object)]]) – A dictionary of diagnoses
  * **pkg_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The name of the package to diagnose
* **Returns:**
  A generator of the results of the diagnoses

Really, just goes through all (name, diagnosis_func) pairs in the diagnoses and
applies the diagnosis_func to the pkg_name, yielding the (name, result) pairs.

Here’s an example using simple functions applied to the string ‘pipoke’
(but obviously, the intended use is to apply functions that actually analyze the
package bearing the name pkg_name):

```pycon
>>> pkg_name = 'pipoke'
>>> diagnoses = {'length': len, 'first_letter': lambda x: x[0]}
>>> dict(generate_diagnoses(pkg_name, diagnoses))
{'length': 6, 'first_letter': 'p'}
```

### pipoke.pkg_diagnosis.get_pyenv_virtualenv_path(virtual_environment_name)

Get the path of a virtual environment managed by pyenv given its name.

### pipoke.pkg_diagnosis.install_package(pkg_name, virtual_env=None, , verbose=True)

Install a package in the virtual environment if not already installed.

### pipoke.pkg_diagnosis.is_package_installed(pkg_name)

Check if a package is installed in the virtual environment.

`pkg_name` can be a bare distribution name or any pip-installable
requirement string (version specifier, extras, environment markers).

### pipoke.pkg_diagnosis.json_package_info(package, url_pattern='https://pypi.python.org/pypi/{package}/json')

Return version of package on pypi.python.org using json.

Makes a real HTTPS request to PyPI, so this example is illustrative only
and is skipped by the doctest runner (pipoke#6): a PyPI outage or a
network-restricted CI runner must not fail the test suite. See
`pipoke.tests.test_pkg_diagnosis.test_json_package_info` for a
network-free, mocked equivalent.

```pycon
>>> d = json_package_info('ps')
>>> isinstance(d, dict)
True
>>> {'name', 'author', 'version'}.issubset(d['info'])
True
```

### pipoke.pkg_diagnosis.pyenv_exists()

Check if pyenv is installed.

### pipoke.pkg_diagnosis.run_folder_diagnosis(pkg_name, folder_diagnosis=<function dflt_folder_diagnosis>)

Run a diagnosis function on the folder containing the package’s code folder.

### pipoke.pkg_diagnosis.run_pkg_diagnosis(pkg_name, pkg_diagnosis=<function dflt_pkg_diagnosis>)

Run a diagnosis function on the imported package.

### pipoke.pkg_diagnosis.run_pkg_tests(pkg_name, virtual_env=None)

Run tests (including doctests, unittest tests, and pytest tests) for the installed package.

### pipoke.pkg_diagnosis.virtualenv_manager(virtual_env, virtual_envs_dir='')

Check if a virtual environment was created using a specific manager,
returning the name of the manager if found.

* **Parameters:**
  * **virtual_env** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The name of the virtual environment
  * **virtual_envs_dir** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The directory where virtual environments are stored
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`None`](https://docs.python.org/3/builtins/constants.html#None)
* **Returns:**
  The name of the virtual environment manager if found, None otherwise

### pipoke.pkg_diagnosis.virtualenv_path(virtual_env, virtual_envs_dir='')

Get the path of a virtual environment given its name.
