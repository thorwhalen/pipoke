"""Tools to run on PyPi distribution of packages."""
from string import Formatter

dflt_formatter = Formatter()


def increment_version(version_str):
    version_nums = list(map(int, version_str.split('.')))
    version_nums[-1] += 1
    return '.'.join(map(str, version_nums))


import requests
import json
from packaging.version import parse

URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


# TODO: Use yb or merge functionality there if missing for json_package_info and
#  derivatives.
def json_package_info(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json.

    >>> d = json_package_info('ps')
    >>> isinstance(d, dict)
    True
    >>> {'name', 'author', 'version'}.issubset(d['info'])
    True

    """
    response = requests.get(url_pattern.format(package=package))
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return dict()


package_info = json_package_info


def _is_package_info_dict(package_info):
    # TODO: make it stronger, verifying the presence of required fields
    return isinstance(package_info, dict)


def ensure_json_package_info(package_info):
    """
    Gets and validates package info dicts from various sources.

    Namely, this is used in functions like ``releases``, ``release_dates`` etc. so
    that we can use them bother as fetcher+parser and as  parsers (giving them the
    same info dict we already fetched, so we don't have to fetch the info twice).
    """
    if isinstance(package_info, str):
        package_name = package_info
        package_info = json_package_info(package_name)
    assert _is_package_info_dict(
        package_info
    ), f'Not a valid package_info_ dict: {package_info}'
    return package_info


def release_versions(package):
    d = ensure_json_package_info(package)
    return list(d)


def release_dates(package):
    d = ensure_json_package_info(package)
    return [dd[-1]['upload_time'] for dd in d['releases'].values()]


def last_release_date(package):
    return release_dates(package)[-1]


def get_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json.

    >>> get_version('py2store')  # doctest: +SKIP
    '0.1.15'

    """
    req = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text)
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version.base_version


def my_setup(**setup_kwargs):
    from setuptools import setup
    import json

    print('Setup params -------------------------------------------------------')
    print(json.dumps(setup_kwargs, indent=2))
    print('--------------------------------------------------------------------')
    setup(**setup_kwargs)


def ujoin(*args):
    """Join strings with the url seperator (/).

    Note that will add a / where it's missing (as in between 'https://pypi.org' and 'project/'),
    and only use one if two consecutive tokens use respectively end and start with a /
    (as in 'project/' and '/pipoke/').

    >>> ujoin('https://pypi.org', 'project/', '/pipoke/')
    'https://pypi.org/project/pipoke/'

    Extremal cases
    >>> ujoin('https://pypi.org')
    'https://pypi.org'
    >>> ujoin('https://pypi.org/')
    'https://pypi.org/'
    >>> ujoin('')
    ''
    >>> ujoin()
    ''
    """
    if len(args) == 0 or len(args[0]) == 0:
        return ''
    return (
        (args[0][0] == '/') * '/'  # prepend slash if first arg starts with it
        + '/'.join(x[(x[0] == '/') : (len(x) - (x[-1] == '/'))] for x in args)
        + (args[-1][-1] == '/') * '/'
    )  # append slash if last arg ends with it



########### Partial and incremental formatting ##########################################
class PartialFormatter(Formatter):
    """A string formatter that won't complain if the fields are only partially formatted.
    But note that you will lose the spec part of your template (e.g. in {foo:1.2f},
    you'll loose the 1.2f if not foo is given -- but {foo} will remain).
    """

    def get_value(self, key, args, kwargs):
        try:
            return super().get_value(key, args, kwargs)
        except KeyError:
            return '{' + key + '}'

    def format_fields_set(self, s):
        return {x[1] for x in self.parse(s) if x[1]}


partial_formatter = PartialFormatter()


# TODO: For those who love algorithmic optimization, there's some wasted to cut out here below.


def _unformatted(d):
    for k, v in d.items():
        if isinstance(v, str) and len(partial_formatter.format_fields_set(v)) > 0:
            yield k


def _fields_to_format(d):
    for k, v in d.items():
        if isinstance(v, str):
            yield from partial_formatter.format_fields_set(v)


def format_str_vals_of_dict(d, *, max_formatting_loops=10, **kwargs):
    """
    Traverse the values of a dict and apply string formatting to them, recursively.

    :param d: The template dict containing both format strings to be populated/embodied
    and (possibly) values to do so.
    :param max_formatting_loops: The maximum number of loops.
    :param kwargs: Extra values to use to populate string formats
    :return: A (shallow) copy of the filled out (i.e. populated/embodied) dict

    >>> d = {
    ...     'filepath': '{root}/{file}.{ext}',
    ...     'ext': 'txt'
    ... }
    >>> format_str_vals_of_dict(d, root='ROOT', file='FILE')
    {'filepath': 'ROOT/FILE.txt', 'ext': 'txt'}

    Note that if the input mapping `d` and the kwargs have a conflict, the mapping
    version is used!

    >>> format_str_vals_of_dict(d, root='ROOT', file='FILE', ext='will_not_be_used')
    {'filepath': 'ROOT/FILE.txt', 'ext': 'txt'}

    But if you want to override an input mapping, you can -- the usual way:

    >>> format_str_vals_of_dict(dict(d, ext='will_be_used'), root='ROOT', file='FILE')
    {'filepath': 'ROOT/FILE.will_be_used', 'ext': 'will_be_used'}

    If you don't provide enough fields to satisfy all the format fields in the values
    of ``d``, you'll be told to bugger off.

    >>> format_str_vals_of_dict(d, root='ROOT')
    Traceback (most recent call last):
    ...
    ValueError: I won't be able to complete that. You'll need to provide the values for:
      file

    And it's recursive...

    >>> d = {
    ...     'filepath': '{root}/{filename}',
    ...     'filename': '{file}.{ext}'
    ... }
    >>> my_configs = {'root': 'ROOT', 'file': 'FILE', 'ext': 'EXT'}
    >>> format_str_vals_of_dict(d, **my_configs)
    {'filepath': 'ROOT/FILE.EXT', 'filename': 'FILE.EXT'}

    # TODO: Could make the above work if filename is give, but not file nor ext!
    #  At least as an option.

    """
    d = dict(**d)  # make a shallow copy
    # The defaults (kwargs) cannot overlap with any keys of d, so:
    kwargs = {k: kwargs[k] for k in set(kwargs) - set(d)}

    provided_fields = set(d) | set(kwargs)
    missing_fields = set(_fields_to_format(d)) - provided_fields

    if missing_fields:
        raise ValueError(
            "I won't be able to complete that. You'll need to provide the values for:\n"
            + f"  {', '.join(missing_fields)}"
        )

    for i in range(max_formatting_loops):
        unformatted = set(_unformatted(d))

        if unformatted:
            for k in unformatted:
                d[k] = partial_formatter.format(d[k], **kwargs, **d)
        else:
            break
    else:
        raise ValueError(
            f'There are still some unformatted fields, '
            f'but I reached my max {max_formatting_loops} allowed loops. '
            + f'Those fields are: {set(_fields_to_format(d)) - (set(d) | set(kwargs))}'
        )

    return d
