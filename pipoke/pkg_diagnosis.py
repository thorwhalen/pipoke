"""Pip installed package diagnosis
The tools here will help you install and diagnose packages in a test virtual 
environment.

Here, checkout diagnose_pkgs, which takes a list of packages and runs a list of
diagnoses on each package, returning a dictionary of the results.
This functionality is also available from the command line using the script
diagnose_pkgs.py (or the shell script diagnose-pkgs).

"""

import os
import sys
import subprocess
import pkg_resources
import json
from typing import (
    Union,
    Iterable,
    Tuple,
    Callable,
    Dict,
    Mapping,
    Protocol,
    runtime_checkable,
)


def current_virtual_environment_path():
    """
    Returns the path of the current virtual environment the function is called from
    """
    return os.environ.get('VIRTUAL_ENV', None)


DFLT_TEST_ENV = current_virtual_environment_path()


def venv_virtualenv_exists(virtual_env):
    return os.path.isdir(virtual_env)


def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))


def virtualenv_path(virtual_env, virtual_envs_dir=''):
    """
    Get the path of a virtual environment given its name.
    """
    return fullpath(os.path.join(virtual_envs_dir or '', virtual_env))


def create_virtualenv(
    virtual_env=DFLT_TEST_ENV,
    virtual_envs_dir='',
):
    """
    Create a virtual environment using specified managers if it doesn't exist.

    :param virtual_env: The path to the virtual environment
    :return True if the virtual environment exists or was created successfully, False otherwise
    """
    virtual_env = virtualenv_path(virtual_env, virtual_envs_dir=virtual_envs_dir)

    if venv_virtualenv_exists(virtual_env):
        print(f"INFO: Virtual environment already exists: {virtual_env}")
    else:
        print(f"INFO: Creating virtual environment: {virtual_env}")
        subprocess.run([sys.executable, '-m', 'venv', virtual_env], check=True)

    return virtual_env  # Exit the function if venv succeeded


def activate_virtualenv(virtualenv_path):
    """
    Activate a virtual environment given its path.
    """
    # Determine the current shell
    shell = os.path.basename(os.getenv('SHELL'))

    if shell in ('bash', 'zsh'):
        activation_script = 'activate'
    elif shell == 'fish':
        activation_script = 'activate.fish'
    elif sys.platform == 'win32':
        activation_script = 'Scripts/activate.bat'
    else:
        raise NotImplementedError("Unsupported shell or platform")

    activation_script_path = os.path.join(virtualenv_path, activation_script)

    # Check if the activation script exists
    if not os.path.exists(activation_script_path):
        raise FileNotFoundError(
            f"Activation script not found: {activation_script_path}"
        )

    # Activate the virtual environment
    try:
        subprocess.run(f"source {activation_script_path}", shell=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to activate the virtual environment")


def install_package(pkg_name, virtual_env=DFLT_TEST_ENV, *, verbose=True):
    """
    Install a package in the virtual environment if not already installed.
    """
    try:
        capture_output = not verbose
        subprocess.run(
            [os.path.join(virtual_env, 'bin', 'pip'), 'install', pkg_name],
            capture_output=capture_output,
            check=True,
        )
    except subprocess.CalledProcessError:
        pass


def is_package_installed(pkg_name):
    """
    Check if a package is installed in the virtual environment.
    """
    try:
        pkg_resources.get_distribution(pkg_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False


def dflt_pkg_diagnosis(imported_pkg):
    non_dunder_attributes = [
        attr for attr in dir(imported_pkg) if not attr.startswith('__')
    ]
    return {
        'non_dunder_attributes_count': len(non_dunder_attributes),
    }


def run_pkg_diagnosis(pkg_name, pkg_diagnosis=dflt_pkg_diagnosis):
    """
    Run a diagnosis function on the imported package.
    """
    try:
        imported_pkg = __import__(pkg_name)
        return pkg_diagnosis(imported_pkg)
    except ImportError:
        return None


def dflt_folder_diagnosis(pkg_folder):
    total_files = sum(len(files) for _, _, files in os.walk(pkg_folder))
    total_bytes = sum(
        os.path.getsize(os.path.join(root, file))
        for root, _, files in os.walk(pkg_folder)
        for file in files
    )

    return {
        'total_files': total_files,
        'total_bytes': total_bytes,
        # Add other useful information here
    }


def run_folder_diagnosis(pkg_name, folder_diagnosis=dflt_folder_diagnosis):
    """
    Run a diagnosis function on the folder containing the package's code folder.
    """
    try:
        pkg_info = pkg_resources.get_distribution(pkg_name)
        pkg_location = pkg_info.location
        pkg_folder = os.path.join(pkg_location, pkg_name.replace('-', '_'))

        return folder_diagnosis(pkg_folder)
    except pkg_resources.DistributionNotFound:
        print(f"ERROR: Package not found: {pkg_name}")
        return None


import subprocess


def run_pkg_tests(pkg_name, virtual_env=DFLT_TEST_ENV):
    """
    Run tests (including doctests, unittest tests, and pytest tests) for the installed package.
    """
    import doctest
    import unittest

    try:
        pkg_info = pkg_resources.get_distribution(pkg_name)
        pkg_location = pkg_info.location
        pkg_folder = os.path.join(pkg_location, pkg_name.replace('-', '_'))

        test_diagnoses = {}

        # Run doctests using doctest module
        try:
            doctest_results = doctest.testmod(pkg_name)
            test_diagnoses['doctest_results'] = {
                'attempts': doctest_results.attempted,
                'failures': doctest_results.failed,
            }
        except Exception:
            pass

        # Run unittest tests
        loader = unittest.TestLoader()
        suite = loader.discover(pkg_folder, pattern="test_*.py")
        unittest_runner = unittest.TextTestRunner(verbosity=2)
        unittest_result = unittest_runner.run(suite)
        test_diagnoses['unittest_results'] = {
            'total_tests_found': unittest_result.testsRun,
            'total_failures': len(unittest_result.failures),
            'total_errors': len(unittest_result.errors),
        }

        try:
            # Run pytest tests within the virtual environment
            cmd = [
                os.path.join(virtual_env, 'bin', 'python'),
                '-m',
                'pytest',
                pkg_folder,
            ]
            # Capture the output for analysis if needed
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            # Analyze the pytest output, parse the results, and extract relevant information
            # Example: You can count the number of passed and failed tests from the output
            # Sample code to count passed and failed tests (modify as needed)
            passed_tests = result.stdout.count("PASSED")
            failed_tests = result.stdout.count("FAILED")

            # Get test diagnoses
            test_diagnoses['pytest_results'] = {
                'total_tests_found': passed_tests + failed_tests,
                'total_passed_tests': passed_tests,
                'total_failed_tests': failed_tests,
            }
        except subprocess.CalledProcessError or Exception:
            pass

        return test_diagnoses

    except pkg_resources.DistributionNotFound:
        return None


URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


# Note: Also found in pipoke.distribution and yb package
def json_package_info(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json.

    >>> d = json_package_info('ps')
    >>> isinstance(d, dict)
    True
    >>> {'name', 'author', 'version'}.issubset(d['info'])
    True

    """
    import requests

    response = requests.get(url_pattern.format(package=package))
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return dict()


def dflt_json_info_extractor(pkg_name):
    from dol import path_get

    info_dict = json_package_info(pkg_name)
    extractor = path_get.paths_getter(
        [
            'info.description',
            'info.summary',
            'info.author',
            'info.version',
            'info.project_urls',
            'info.home_page',
            'releases',
        ],
        on_error=path_get.return_none_on_error,
    )
    d = extractor(info_dict)
    releases = d.pop('releases', ())
    d['n_releases'] = len(releases)
    if releases:
        release = next(iter(releases[d['info.version']]), None)
        if release:
            d['last_release.size'] = release.get('size', None)
            d['last_relase.upload_time_iso_8601'] = release.get(
                'upload_time_iso_8601', None
            )
    return d


DiagnosisPair = Tuple[str, Callable[[str], object]]
DiagnosisPairs = Iterable[DiagnosisPair]
DiagnosisDict = Dict[str, object]
Diagnoses = Union[DiagnosisPairs, DiagnosisDict]


# default diagnoses,
# as a tuple of (name, diagnosis_func) pairs because python still has no frozendict!
DFLT_DIAGNOSES = (
    ('json_info', dflt_json_info_extractor),
    ('pkg_diagnosis_result', run_pkg_diagnosis),
    ('pkg_folder_diagnosis_result', run_folder_diagnosis),
    ('test_diagnosis_result', run_pkg_tests),
)

diagnosis_funcs = dict(DFLT_DIAGNOSES)
diagnosis_funcs['all_json_info'] = json_package_info


def _resolve_diagnoses(diagnoses: Diagnoses) -> DiagnosisDict:
    if not isinstance(diagnoses, Mapping):
        if isinstance(diagnoses, str):
            diagnoses = [diagnoses]

        def resolve_string_diagnoses(diagnoses):
            for d in diagnoses:
                if isinstance(d, str):
                    name = d
                    if name in diagnosis_funcs:
                        yield name, diagnosis_funcs[name]
                    else:
                        raise ValueError(f"Unknown diagnosis name: {name}")
                else:
                    yield d  # assume it's a diagnosis pair

        diagnoses = dict(resolve_string_diagnoses(diagnoses))

    return diagnoses


def _resolve_packages(pkgs: Union[str, Iterable[str]]):
    """Resolve a string of packages or a filepath to a requirements file
    to a list of packages"""
    if isinstance(pkgs, str):
        if os.path.isfile(pkgs):
            with open(pkgs) as f:
                pkgs = f.readlines()
        else:
            pkgs = pkgs.split()
    return pkgs


@runtime_checkable
class Settable(Protocol):
    """A protocol for objects obj that support obj[k] = v"""

    def __setitem__(self, k, v):
        """The method controlling self[k] = v"""


def _resolve_store_factory(store_factory: Union[str, Callable[[], Settable]]):
    if isinstance(store_factory, str):
        if store_factory == 'dict':
            store_factory = dict
        elif os.path.isdir(store_factory):
            dirpath = store_factory
            from dol import Jsons

            store_factory = lambda: Jsons(dirpath)
        else:
            raise ValueError(
                f"Unknown store factory (if it's a folder, it doesn't exist: "
                f"{store_factory}"
            )
    return store_factory


def diagnose_pkgs(
    pkgs: Union[str, Iterable[str]],
    diagnoses: Union[Diagnoses, Iterable[str]] = DFLT_DIAGNOSES,
    store_factory: Union[str, Callable[[], Settable]] = dict,
):
    """Diagnose a list of packages

    :param pkgs: A list of packages to diagnose (or a filepath to a requirements file)
    :param diagnoses: What diagnoses to run
        (dict, (name, func) pairs, or requirements file)
    :param store_factory: A factory that makes a store to store the results.
        If an (existing) folder path, will be stored in json files under that folder
    """
    pkgs = _resolve_packages(pkgs)
    diagnoses = _resolve_diagnoses(diagnoses)
    store_factory = _resolve_store_factory(store_factory)
    if isinstance(pkgs, str):
        pkgs = pkgs.split()
    d = store_factory()
    for pkg in pkgs:
        d[pkg] = diagnose_pkg(pkg, diagnoses=diagnoses)
    return d


def generate_diagnoses(
    pkg_name: str,
    diagnoses: Diagnoses = DFLT_DIAGNOSES,
    *,
    error_logger: Callable = print,
):
    """Runs through the diagnoses and yields the results.

    :param diagnoses: A dictionary of diagnoses
    :param pkg_name: The name of the package to diagnose
    :return: A generator of the results of the diagnoses

    Really, just goes through all (name, diagnosis_func) pairs in the diagnoses and
    applies the diagnosis_func to the pkg_name, yielding the (name, result) pairs.

    Here's an example using simple functions applied to the string 'pipoke'
    (but obviously, the intended use is to apply functions that actually analyze the
    package bearing the name pkg_name):

    >>> pkg_name = 'pipoke'
    >>> diagnoses = {'length': len, 'first_letter': lambda x: x[0]}
    >>> dict(generate_diagnoses(diagnoses, pkg_name))
    {'length': 6, 'first_letter': 'p'}

    """
    diagnoses = dict(diagnoses)
    for name, diagnosis in diagnoses.items():
        try:
            yield name, diagnosis(pkg_name)
        except Exception as e:
            error_logger(f"ERROR: {pkg_name=}, {name=}: {e}")


import subprocess
from contextlib import contextmanager


@contextmanager
def manage_installation(pkg_name, install_pkg_if_not_installed=True, *, verbose=True):
    try:
        pkg_was_in_environment = False
        if install_pkg_if_not_installed:
            pkg_was_in_environment = is_package_installed(pkg_name)

            # Install the package if not in the environment
            if not pkg_was_in_environment:
                install_package(pkg_name, verbose=verbose)

        yield pkg_was_in_environment

    finally:
        # Uninstall the package if it was installed in this process
        if install_pkg_if_not_installed and not pkg_was_in_environment:
            subprocess.run(
                ['pip', 'uninstall', '-y', pkg_name], capture_output=not verbose
            )


def diagnose_pkg(
    pkg_name: str,
    diagnoses: Diagnoses = DFLT_DIAGNOSES,
    *,
    install_pkg_if_not_installed: bool = True,
    error_logger: Callable = print,
    verbose=True,
):
    """Diagnose a package, given it's name

    :param pkg_name: The name of the package to diagnose
    :param diagnoses: A dictionary of diagnoses (name and function pairs)
    :param install_pkg_if_not_installed: Whether to install the package if it's not installed
    :param error_logger: A function to log errors
    """

    diagnoses = _resolve_diagnoses(diagnoses)

    with manage_installation(pkg_name, install_pkg_if_not_installed, verbose=verbose):
        d = dict(generate_diagnoses(pkg_name, diagnoses, error_logger=error_logger))

    return d


# def diagnose_pkg(
#     pkg_name: str,
#     diagnoses: Diagnoses = DFLT_DIAGNOSES,
#     *,
#     install_pkg_if_not_installed: bool = True,
#     error_logger: Callable = print,
# ):
#     """Diagnose a package, given it's name

#     :param pkg_name: The name of the package to diagnose
#     :param diagnoses: A dictionary of diagnoses (name and function pairs)
#     :param install_pkg_if_not_installed: Whether to install the package if it's not installed
#     :param error_logger: A function to log errors
#     """

#     diagnoses = _resolve_diagnoses(diagnoses)

#     pkg_was_in_environment = False
#     if install_pkg_if_not_installed:
#         pkg_was_in_environment = is_package_installed(pkg_name)

#         # Install the package if not in the environment
#         if not pkg_was_in_environment:
#             install_package(pkg_name)

#     d = dict(generate_diagnoses(pkg_name, diagnoses, error_logger=error_logger))

#     # Uninstall the package if it was installed in this process
#     if install_pkg_if_not_installed and not pkg_was_in_environment:
#         subprocess.run(['pip', 'uninstall', '-y', pkg_name])

#     return d

# Extras for pyenv:


def virtualenv_manager(
    virtual_env: str,
    virtual_envs_dir: str = '',  # empty string will have the effect of looking in the current directory
) -> Union[str, None]:
    """
    Check if a virtual environment was created using a specific manager,
    returning the name of the manager if found.

    :param virtual_env: The name of the virtual environment
    :param virtual_envs_dir: The directory where virtual environments are stored
    :return: The name of the virtual environment manager if found, None otherwise

    """
    virtual_envs_dir = virtual_envs_dir or ''
    virtual_env_path = os.path.join(virtual_envs_dir, virtual_env)
    # Check if it's a venv-created virtual environment
    venv_marker = os.path.join(virtual_env_path, 'pyvenv.cfg')
    if os.path.exists(venv_marker):
        return 'venv'

    # Check if it's a pyenv-created virtual environment
    pyenv_version_file = os.path.join(virtual_env_path, '.python-version')
    if os.path.exists(pyenv_version_file):
        return 'pyenv'

    return None


def pyenv_exists():
    """
    Check if pyenv is installed.
    """
    try:
        subprocess.run(['pyenv', '--version'], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False


def create_virtualenv_with_pyenv(virtual_environment_name):
    """
    Create a virtual environment using pyenv if it doesn't exist.

    :param virtual_environment_name: The name of the virtual environment
    :return True if the virtual environment exists or was created successfully, False otherwise
    """
    # Check if pyenv is installed
    if not pyenv_exists():
        raise ValueError("ERROR: pyenv not found")

    # Check if the virtual environment exists
    virtualenv_path = get_pyenv_virtualenv_path(virtual_environment_name)
    if virtualenv_path:
        print(f"INFO: Virtual environment already exists: {virtualenv_path}")
        return virtualenv_path

    # Create the virtual environment
    try:
        subprocess.run(['pyenv', 'virtualenv', virtual_environment_name], check=True)
        return get_pyenv_virtualenv_path(virtual_environment_name)
    except subprocess.CalledProcessError:
        return False


def activate_virtualenv_with_pyenv(virtual_environment_name):
    """
    Activate a virtual environment using pyenv given its name.
    """
    # Check if pyenv is installed
    if not pyenv_exists():
        raise ValueError("ERROR: pyenv not found")

    # Check if the virtual environment exists
    virtualenv_path = get_pyenv_virtualenv_path(virtual_environment_name)
    if not virtualenv_path:
        raise ValueError(
            f"ERROR: Virtual environment not found: {virtual_environment_name}"
        )

    # Activate the virtual environment
    try:
        subprocess.run(['pyenv', 'activate', virtual_environment_name], check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to activate the virtual environment")


def get_pyenv_virtualenv_path(virtual_environment_name):
    """
    Get the path of a virtual environment managed by pyenv given its name.
    """
    try:
        # Run the pyenv virtualenv-prefix command and capture the output
        cmd = ['pyenv', 'virtualenv-prefix', virtual_environment_name]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        # Check if the command was successful and has output
        if result.returncode == 0 and result.stdout:
            return (
                result.stdout.strip()
            )  # Remove leading/trailing whitespace and return the path
        else:
            return None  # Return None if the command fails or has no output
    except FileNotFoundError:
        # Handle the case where pyenv is not found
        return None


import yp


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Run package diagnosis on a list of packages'
    )
    parser.add_argument(
        'packages',
        metavar='package',
        type=str,
        nargs='+',
        help=(
            'The names of the packages to diagnose. Could be a single package name or '
            'multiple package names separated by strings. Could also be a local '
            'filepath to a requirements file (any file whose lines are pip installable)'
        ),
    )
    diagnoses_names = ', '.join(name for name, _ in diagnosis_funcs)
    parser.add_argument(
        '--diagnoses',
        type=str,
        nargs='+',
        help=(
            f'The names of the diagnoses to run. Any combination of: {diagnoses_names}. '
            'If not specified, all diagnoses will be run.'
        ),
    )
    parser.add_argument(
        '--store_factory',
        type=str,
        default='dict',
        help=(
            'A factory for a store to store the results. '
            'Can be a folder path (in which case a Files store will be created in that folder), '
            'or "dict" (in which case a dict will be used), '
            'or any other string (in which case a dict will be used).'
        ),
    )
    parser.add_argument(
        '--install_pkg_if_not_installed',
        type=bool,
        default=True,
        help='Whether to install the package if it is not installed',
    )
    parser.add_argument(
        '--verbose',
        type=bool,
        default=True,
        help='Whether to print verbose output',
    )

    args = parser.parse_args()

    # run diagnose_pkgs
    d = diagnose_pkgs(args.packages, args.diagnoses)

    # print the results
    print('------ RESULTS ------')
    print(json.dumps(d, indent=2))


# script to run diagnose_pkgs from the command line
if __name__ == '__main__':
    main()
