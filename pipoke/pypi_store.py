import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from functools import wraps
import tempfile
import pickle
import re

from pipoke import dpath

pkg_list_url = 'https://pypi.org/simple'
pkg_info_furl = 'https://pypi.python.org/pypi/{pkg_name}/json'
pkg_names_filepath = dpath('pkg_list.p')
pkg_name_re = re.compile('/simple/([^/]+)/')

try:
    pkg_name_stub = pickle.load(open(pkg_names_filepath, 'rb'))
except:
    import warnings

    warnings.warn(f"Couldn't unpickle {pkg_names_filepath}. Some functionality might not work")


@wraps(requests.request)
def request_saving_failure_responses(*args, **kwargs):
    r = requests.request(*args, **kwargs)
    if r.status_code == 200:
        return r
    else:
        msg = f"Request came back with status_code: {r.status_code}"
        tmp_filepath = tempfile.mktemp()
        pickle.dump(r, open(tmp_filepath, 'wb'))
        msg += f'''\nThe response object was pickled in {tmp_filepath}.
        To get it do:
        import pickle
        r = pickle.load(open('{tmp_filepath}', 'rb'))
        '''
        raise RequestException(msg)


@wraps(BeautifulSoup.find_all, assigned=('__module__', '__qualname__', '__annotations__', '__name__'))
def gen_find(tag, *args, **kwargs):
    """Does what BeautifulSoup.find_all does, but as an iterator.
        See find_all documentation for more information."""
    if isinstance(tag, str):
        tag = BeautifulSoup(tag, features="lxml")
    next_tag = tag.find(*args, **kwargs)
    while next_tag is not None:
        yield next_tag
        next_tag = next_tag.find_next(*args, **kwargs)


def get_updated_pkg_name_stub():
    """
    Get {pkg_name: pkg_stub} data from pypi
    :return: {pkg_name: pkg_stub, ...} dict
    """
    r = request_saving_failure_responses('get', pkg_list_url)
    t = BeautifulSoup(r.content.decode(), features="lxml")
    return {str(x.contents[0]).lower(): pkg_name_re.match(x.get('href')).group(1) for x in gen_find(t, 'a')}


def refresh_saved_pkg_name_stub():
    """
    Update the {pkg_name: pkg_stub} stored data with a fresh call to get_updated_pkg_name_stub
    """
    pkg_name_stub = get_updated_pkg_name_stub()
    pickle.dump(pkg_name_stub, open(pkg_names_filepath, 'wb'))


def info_of_pkg_from_web(pkg_name):
    """
    Get dict of information for a pkg_name
    :param pkg_name:
    :return:
    """
    r = request_saving_failure_responses('get', pkg_info_furl.format(pkg_name=pkg_name))
    return r.json()


if __name__ == '__main__':
    import argh

    parser = argh.ArghParser()
    parser.add_commands([get_updated_pkg_name_stub, refresh_saved_pkg_name_stub, info_of_pkg_from_web])
    parser.dispatch()
