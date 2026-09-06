"""Tests for :mod:`pipoke.pkg_diagnosis`.

These guard against the package becoming unimportable because of a dependency
on ``pkg_resources``, which setuptools stopped shipping in version 81.
"""

import importlib
import pkgutil

import pipoke
from pipoke.pkg_diagnosis import is_package_installed

# A distribution that is always present when the test suite runs, and one that
# cannot reasonably exist on PyPI or in any environment.
AN_INSTALLED_PKG = 'pytest'
A_MISSING_PKG = 'a-package-that-does-not-exist-xyz'

# Subpackages that are not part of the importable surface of the package.
NON_LIBRARY_SUBMODULES = ('examples', 'scrap', 'tests')


def test_package_is_importable():
    """The top-level package imports without any setuptools runtime."""
    assert pipoke.__all__


def test_submodules_are_importable():
    """Every library submodule imports, not just the top-level package."""
    for module_info in pkgutil.iter_modules(pipoke.__path__):
        name = module_info.name
        if name.startswith('_') or name in NON_LIBRARY_SUBMODULES:
            continue
        importlib.import_module(f'pipoke.{name}')


def test_is_package_installed():
    """Installed distributions are found; missing ones are reported missing."""
    assert is_package_installed(AN_INSTALLED_PKG) is True
    assert is_package_installed(A_MISSING_PKG) is False
