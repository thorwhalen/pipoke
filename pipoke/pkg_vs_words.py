import inspect
import re
import pickle

from pipoke import dpath
from pipoke.pypi_store import pkg_name_stub


def get_all_words_from_wordnet():
    from nltk.corpus import wordnet as wn
    return set(wn.all_lemma_names())


try:
    all_words = pickle.load(open(dpath('all_words.p'), 'rb'))
except:
    all_words = get_all_words_from_wordnet()

pkg_names = set(pkg_name_stub)
pkg_names_that_are_words = all_words.intersection(pkg_names)


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
    return words_and_pkg_names_satisfying_condition(re.compile(regex).match, regex, print_counts)


def is_not_a_pkg_name(words):
    if isinstance(words, str):
        words = set(map(lambda w: w.strip(), words.split(',')))
    return set(words).difference(pkg_names)


if __name__ == '__main__':
    import argh

    parser = argh.ArghParser()


    def allwords():
        return all_words


    def pkgnames():
        return pkg_names


    parser.add_commands([words_and_pkg_names_satisfying_regex, is_not_a_pkg_name, allwords, pkgnames])
    parser.dispatch()
