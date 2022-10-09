"""
A mapping view to pypi projects
Is now maintained in the ``https://pypi.org/project/yp/`` project.

Three functions are exposed as scripts here:
    get_updated_pkg_name_stub,
    refresh_saved_pkg_name_stub, and
    info_of_pkg_from_web

"""

from yp.base import *


if __name__ == '__main__':
    import argh

    parser = argh.ArghParser()
    parser.add_commands(
        [get_updated_pkg_name_stub, refresh_saved_pkg_name_stub, info_of_pkg_from_web]
    )
    parser.dispatch()
