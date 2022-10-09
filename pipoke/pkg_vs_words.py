import inspect
import re
import pickle
import pkgutil
import builtins
import os

from pipoke import dpath
from pipoke.pypi_store import pkg_name_stub

standard_lib_dir = os.path.dirname(os.__file__)


def is_standard_lib_path(path):
    return path.startswith(standard_lib_dir)


def standard_lib_module_names(is_standard_lib_path=is_standard_lib_path,
                              name_filt=lambda name: not name.startswith('_')):
    return filter(name_filt, (module_info.name for module_info in pkgutil.iter_modules()
                              if is_standard_lib_path(module_info.module_finder.path)))


local_pkg_names = {x.name for x in pkgutil.iter_modules() if x.ispkg}

builtin_pkg_names = set(standard_lib_module_names())
builtin_obj_names = {x.lower() for x in dir(builtins)}

py_reserved_words = {
    'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
    'except', 'exec', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass',
    'print', 'raise', 'return',
    'try', 'while', 'with', 'yield'
}

builtin_names = builtin_pkg_names | builtin_obj_names | py_reserved_words


def get_all_words_from_wordnet():
    from nltk.corpus import wordnet as wn
    return set(wn.all_lemma_names())


try:
    all_words = pickle.load(open(dpath('all_words.p'), 'rb'))
except:
    all_words = get_all_words_from_wordnet()

simple_words = set(filter(re.compile('[a-z]+$').match, all_words))

pypi_pkg_names = set(pkg_name_stub)
pkg_names = pypi_pkg_names.union(builtin_names)  # pypi + builtin pkg names
pkg_names_that_are_words = all_words.intersection(pkg_names)

available_simple_words = simple_words - pkg_names


def str_for_func(func):
    s = func.__name__
    if s != '<lambda>':
        return s
    else:
        fs = inspect.getsource(func)
        fs = fs[:fs.index('\n')]
        lambda_re = re.compile('.+lambda (.+)')
        return lambda_re.match(fs).group(1)


def disp_str_for_counts(words, pkgs, pkgs_words):
    s = ''
    s += f"{len(words)} words"
    s += f"{len(pkgs)} package names"
    s += f"{len(pkgs_words)} that are both"
    return s


def words_and_pkg_names_satisfying_condition(cond, print_counts=False, cond_str=None):
    words = list(filter(cond, all_words))
    pkgs = list(filter(cond, pkg_names))
    pkgs_words = list(filter(cond, pkg_names_that_are_words))
    if print_counts:
        if cond_str is None:
            cond_str = str_for_func(cond)
        print(f"{cond_str}")
        print(disp_str_for_counts(words, pkgs, pkgs_words))
    return words, pkgs, pkgs_words


def words_and_pkg_names_satisfying_regex(regex, print_counts=False):
    """
    Get (English) words, pypi package names, and strings that are both words and package names.
    :param regex: Regular expression that should match the WHOLE string
    :param print_counts: Print count statistics
    :return:
    """
    return words_and_pkg_names_satisfying_condition(re.compile(regex).match, print_counts=print_counts, cond_str=regex)


def is_not_a_pkg_name(regex='.*', words=None):
    """
    Filter words, keeping only those that are not already pypi package names.
    :param regex: Extra (regular expression) filter to apply
    :param words: The words you want to filter. By default will take all (simple) words of the (wordnet) dictionary.
    :return: The subset of input words that are not pypi package names
    """
    words = words or simple_words
    if isinstance(words, str):
        words = set(map(lambda w: w.strip(), words.split(',')))
    return set(filter(re.compile(regex).match, words)).difference(pkg_names)


if __name__ == '__main__':
    import argh

    parser = argh.ArghParser()


    def allwords():
        return all_words


    def pkgnames():
        return pkg_names


    parser.add_commands([words_and_pkg_names_satisfying_regex, is_not_a_pkg_name, allwords, pkgnames])
    parser.dispatch()
