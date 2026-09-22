"""Tests for :mod:`pipoke.pkg_diagnosis`.

Two things are guarded here.

*The package stays importable.* ``pkg_resources`` was removed in setuptools 81,
and :mod:`pipoke.pkg_diagnosis` used to import it at module scope, which made
every pipoke submodule dead on a modern setuptools. The guard is static (it
reads the source) rather than dynamic, because a test that merely imports
pipoke only goes red in an environment that already lacks ``pkg_resources`` --
notably not on CI, whose Python still bundles an old enough setuptools.

*Requirement strings still resolve.* ``pkg_resources.get_distribution`` parsed
its argument as a PEP 508 requirement; ``importlib.metadata.distribution``
looks up a literal name. ``diagnose_pkgs`` documents a requirements file as
valid input, so version specifiers, extras, markers and padded names must keep
working -- and a false "not installed" is destructive here, because
``manage_installation`` uninstalls afterwards whatever it believes it installed.
"""

import ast
import importlib
import os
import pkgutil
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

import pipoke
from pipoke.pkg_diagnosis import (
    _pkg_folder,
    is_package_installed,
    json_package_info,
    run_folder_diagnosis,
    run_pkg_tests,
)

PKG_DIR = Path(pipoke.__file__).parent

#: Removed in setuptools 81; no pipoke module may import it.
FORBIDDEN_MODULE = 'pkg_resources'

#: A distribution that is always present when the test suite runs, and one that
#: cannot reasonably exist in any environment.
AN_INSTALLED_PKG = 'pytest'
A_MISSING_PKG = 'a-package-that-does-not-exist-xyz'

#: Subpackages that are not part of the importable surface of the package.
NON_LIBRARY_SUBMODULES = ('examples', 'scrap', 'tests')

#: Requirement shapes ``pkg_resources.get_distribution`` used to accept. Each
#: names ``AN_INSTALLED_PKG``, so each must resolve to it.
INSTALLED_REQUIREMENT_SHAPES = (
    'pytest',
    'pytest>=1.0',
    'pytest >= 1.0',
    'pytest[an-extra]',
    'pytest ; python_version > "3"',
    '  pytest  ',
    'pytest\n',
    'PyTest',
)


def _imported_module_names(source: str):
    """Yield the dotted name of every module imported by a python source."""
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            if node.module is not None:
                yield node.module


def _imports(py_file: Path, module_name: str) -> bool:
    source = py_file.read_text(encoding='utf-8')
    return any(
        imported == module_name or imported.startswith(f'{module_name}.')
        for imported in _imported_module_names(source)
    )


def test_no_module_imports_pkg_resources():
    """No pipoke module may depend on the setuptools runtime."""
    scanned = sorted(PKG_DIR.rglob('*.py'))
    assert scanned, f'no python files found under {PKG_DIR}'
    offenders = [
        str(py_file.relative_to(PKG_DIR))
        for py_file in scanned
        if _imports(py_file, FORBIDDEN_MODULE)
    ]
    assert not offenders, (
        f'{FORBIDDEN_MODULE} was removed in setuptools 81, so importing it makes'
        f' every pipoke module unimportable. Offending modules: {offenders}'
    )


def test_advertised_names_are_all_resolvable():
    """Every name in ``__all__`` is actually reachable on the package."""
    missing = [name for name in pipoke.__all__ if not hasattr(pipoke, name)]
    assert not missing, f'names in pipoke.__all__ that do not resolve: {missing}'


def test_submodules_are_importable():
    """Every library submodule imports, not just the top-level package."""
    imported = []
    for module_info in pkgutil.iter_modules(pipoke.__path__):
        name = module_info.name
        if name.startswith('_') or name in NON_LIBRARY_SUBMODULES:
            continue
        importlib.import_module(f'pipoke.{name}')
        imported.append(name)
    assert imported, 'no pipoke submodules were walked'


@pytest.mark.parametrize('requirement', INSTALLED_REQUIREMENT_SHAPES)
def test_is_package_installed_accepts_requirement_strings(requirement):
    """Anything pip accepts resolves, as it did under ``pkg_resources``."""
    assert is_package_installed(requirement) is True


@pytest.mark.parametrize('requirement', (A_MISSING_PKG, f'{A_MISSING_PKG}>=1.0'))
def test_is_package_installed_reports_missing_packages(requirement):
    assert is_package_installed(requirement) is False


@pytest.mark.parametrize('requirement', ('', '!!!'))
def test_is_package_installed_rejects_malformed_requirements(requirement):
    """Unparseable input raises, rather than being reported as not installed."""
    with pytest.raises(ValueError):
        is_package_installed(requirement)


def test_pkg_folder_is_an_absolute_existing_directory():
    """The location handed to os.walk/subprocesses must not depend on the cwd."""
    pkg_folder = _pkg_folder(AN_INSTALLED_PKG)
    assert os.path.isabs(pkg_folder)
    assert os.path.isdir(pkg_folder)


def test_run_folder_diagnosis_of_installed_package():
    diagnosis = run_folder_diagnosis(AN_INSTALLED_PKG)
    assert diagnosis is not None
    assert diagnosis['total_files'] > 0
    assert diagnosis['total_bytes'] > 0


def test_run_folder_diagnosis_accepts_requirement_strings():
    """A pinned requirement diagnoses the same folder as its bare name."""
    assert run_folder_diagnosis(f'{AN_INSTALLED_PKG}>=1.0') == run_folder_diagnosis(
        AN_INSTALLED_PKG
    )


def test_run_folder_diagnosis_of_missing_package():
    assert run_folder_diagnosis(A_MISSING_PKG) is None


def test_run_pkg_tests_of_missing_package():
    assert run_pkg_tests(A_MISSING_PKG) is None


def test_json_package_info():
    """Network-free equivalent of the (doctest: +SKIP'd) module docstring example.

    Guards pipoke#6: the real doctest hits PyPI over HTTPS, which must never
    gate CI. This mocks ``requests.get`` so the same contract -- a dict with
    an ``info`` sub-dict carrying ``name``/``author``/``version`` -- is
    checked without the network dependency.
    """
    fake_payload = {
        'info': {'name': 'ps', 'author': 'someone', 'version': '1.0'},
    }
    fake_response = Mock(status_code=200, **{'json.return_value': fake_payload})
    with patch('requests.get', return_value=fake_response) as mocked_get:
        d = json_package_info('ps')
    mocked_get.assert_called_once()
    assert isinstance(d, dict)
    assert {'name', 'author', 'version'}.issubset(d['info'])


def test_json_package_info_returns_empty_dict_on_non_ok_status():
    fake_response = Mock(status_code=404)
    with patch('requests.get', return_value=fake_response):
        assert json_package_info('a-package-that-does-not-exist-xyz') == {}
