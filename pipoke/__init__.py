"""pipoke"""

__author__ = 'thorwhalen'

from collections import ChainMap
import os

proj_rootdir = os.path.dirname(__file__)
DFLT_ROOTDIR = proj_rootdir
ROOTDIR_ENV_VAR = 'PIPOKE_ROOTDIR'

resources = ChainMap(os.environ)

rootdir = resources.get(ROOTDIR_ENV_VAR, DFLT_ROOTDIR)

ppath = lambda path='': os.path.join(rootdir, path)
dpath = lambda path='': os.path.join(rootdir, 'data', path)

for _dirpath in [rootdir, dpath()]:
    if not os.path.isdir(_dirpath):
        os.mkdir(_dirpath)

from pipoke.pkg_vs_words import (
    available_simple_words,
    simple_words,
    all_words,
    pypi_pkg_names,
    builtin_pkg_names,
    builtin_obj_names,
    py_reserved_words,
    words_and_pkg_names_satisfying_condition,
    words_and_pkg_names_satisfying_regex,
    is_not_a_pkg_name
)
from pipoke.pypi_store import (
    Pypi,
    pkg_name_stub,
    refresh_saved_pkg_name_stub,
    info_of_pkg_from_web,
    slurp_user_projects_info
)
from pipoke.distribution import (
    get_version,
    json_package_info,
    release_versions,
    release_dates,
    last_release_date,
)

__all__ = [
    "available_simple_words",
    "simple_words",
    "all_words",
    "words_and_pkg_names_satisfying_condition",
    "words_and_pkg_names_satisfying_regex",
    "is_not_a_pkg_name",
    "pkg_name_stub",
    "refresh_saved_pkg_name_stub",
    "info_of_pkg_from_web",
    "get_version"
]
