"""Pip installed package diagnosis
The tools here will help you install and diagnose packages in a test virtual 
environment.
"""

import os
import sys
import subprocess
import pkg_resources
import json
from typing import Union, Iterable


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


def install_package(pkg_name, virtual_env=DFLT_TEST_ENV):
    """
    Install a package in the virtual environment if not already installed.
    """
    try:
        subprocess.run(
            [os.path.join(virtual_env, 'bin', 'pip'), 'install', pkg_name], check=True
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


def diagnose_pkgs(pkgs: Iterable[str]):
    if isinstance(pkgs, str):
        pkgs = pkgs.split()
    d = {}
    for pkg in pkgs:
        d[pkg] = diagnose_pkg(pkg)
    return d


def dflt_json_info_extractor(pkg_name):
    from pipoke.distribution import package_info
    from dol import path_get

    info_dict = package_info(pkg_name)
    extractor = path_get.paths_getter(
        ['info.description', 'info.summary', 'info.author', 'info.version', 'releases'],
        on_error = path_get.return_none_on_error,
    )
    d = extractor(info_dict)
    releases = d.pop('releases')
    if releases:
        release = next(iter(releases[d['info.version']]), None)
        if release:
            d['release.size'] = release['size']
            d['relase.upload_time_iso_8601'] = release['upload_time_iso_8601']
    return d


def diagnose_pkg(
    pkg_name: str,
    # virtual_env: str = DFLT_TEST_ENV,
    # *,
    # virtual_envs_dir: str = '',
    # delete_created_virtual_env_when_done: bool = True,
):
    # Initialize the results with default values
    pkg_was_in_environment = False

    # virtual_env = virtualenv_path(virtual_env, virtual_envs_dir=virtual_envs_dir)
    # virtual_env_existed = venv_virtualenv_exists(virtual_env)

    # # Create the virtual environment if it doesn't exist
    # virtual_env = create_virtualenv(virtual_env)

    # Check if the package is already in the environment
    pkg_was_in_environment = is_package_installed(pkg_name)

    # Install the package if not in the environment
    if not pkg_was_in_environment:
        install_package(pkg_name)

    d = dict()

    try:
        d['pkg_diagnosis_result'] = run_pkg_diagnosis(pkg_name)
    except Exception as e:
        print(f"ERROR: pkg_diagnosis_result: {e}")

    try:
        d['pkg_folder_diagnosis_result'] = run_folder_diagnosis(pkg_name)
    except Exception as e:
        print(f"ERROR: pkg_folder_diagnosis_result: {e}")

    try:
        d['test_diagnosis_result'] = run_pkg_tests(pkg_name)
    except Exception as e:
        print(f"ERROR: test_diagnosis_result: {e}")

    try:
        d['json_info'] = dflt_json_info_extractor(pkg_name)
    except Exception as e:
        print(f"ERROR: json_info: {e}")

    # Uninstall the package if it was installed in this process
    if not pkg_was_in_environment:
        subprocess.run(['pip', 'uninstall', '-y', pkg_name])

    # if delete_created_virtual_env_when_done and not virtual_env_existed:
    #     # Delete the virtual environment if it was created in this process
    #     print(f"DONE: Deleting virtual environment: {virtual_env}")
    #     subprocess.run(['rm', '-rf', virtual_env])

    return d


# def _run_diagnoses(pkg_name):
#     d = {
#         # 'pkg_was_in_environment': pkg_was_in_environment,
#         'pkg_diagnosis_result': run_pkg_diagnosis(pkg_name),
#         'pkg_folder_diagnosis_result': run_folder_diagnosis(pkg_name),
#         'test_diagnosis_result': run_pkg_tests(pkg_name),
#     }

#     return json.dumps(d, indent=2)


# def run_script_in_virtualenv(script_path, virtual_env, *args):
#     python_executable = os.path.join(virtual_env, 'bin', 'python')
#     cmd = [python_executable, script_path] + list(args)
#     result = subprocess.run(
#         cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
#     )
#     return result.stdout


# def run_pkg_diagnosis(pkg_name, virtual_env=DFLT_TEST_ENV):
#     # path to your standalone script for package diagnosis
#     script_path = 'path/to/pkg_diagnosis_script.py'
#     return run_script_in_virtualenv(script_path, virtual_env, pkg_name)


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


# script to run diagnose_pkgs from the command line
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Run package diagnosis on a list of packages'
    )
    parser.add_argument(
        'packages',
        metavar='package',
        type=str,
        nargs='+',
        help='The names of the packages to diagnose',
    )
    parser.add_argument(
        '--virtual-env',
        type=str,
        default=DFLT_TEST_ENV,
        help='The name of the virtual environment to use',
    )
    parser.add_argument(
        '--virtual-envs-dir',
        type=str,
        default='',
        help='The directory where virtual environments are stored',
    )
    parser.add_argument(
        '--delete-created-virtual-env-when-done',
        action='store_true',
        help='Delete the virtual environment when done',
    )
    args = parser.parse_args()

    # run diagnose_pkgs
    d = diagnose_pkgs(args.packages)

    # print the results
    print(json.dumps(d, indent=2))
