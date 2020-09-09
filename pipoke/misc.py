# print('\n'.join(is_not_a_pkg_name('^.+py.+$')))
# print(is_not_a_pkg_name('.*py$'))

from pipoke.pkg_vs_words import *


def is_from_module(obj, module):
    """Check if an object "belongs" to a module.

    >>> import collections
    >>> is_from_module(collections.ChainMap, collections)
    True
    >>> is_from_module(is_from_module, collections)
    False
    """
    return getattr(obj, '__module__', '').startswith(module.__name__)


def second_party_names(module, obj_filt=None):
    """Generator of module attribute names that point to object the module actually defines.

    :param module: Module (object)
    :param obj_filt: Boolean function applied to object to filter it in
    :return:

    >>> from ut.util.code import modules
    >>> sorted(second_party_names(modules))[:5]
    ['DOTPATH', 'FILEPATH', 'FOLDERPATH', 'LOADED', 'ModuleSpecKind']
    >>> sorted(second_party_names(modules, callable))[:5]
    ['ModuleSpecKind', 'coerce_module_spec', 'get_imported_module_paths', 'is_from_module', 'is_module_dotpath']
    >>> sorted(second_party_names(modules, lambda obj: isinstance(obj, type)))
    ['ModuleSpecKind']
    """
    obj_filt = obj_filt or (lambda x: x)
    for attr in filter(lambda a: not a.startswith('_'), dir(module)):
        obj = getattr(module, attr)
        if is_from_module(obj, module) and obj_filt(obj):
            yield attr


n_words = len(simple_words)
n_pkgs = len(pkg_names)


def words_containing_py_free_for_pkg():
    return is_not_a_pkg_name('^.+py.+$')


def words_starting_with_py_free_for_pkg():
    return is_not_a_pkg_name('py.*$')


def words_ending_with_py_free_for_pkg():
    return is_not_a_pkg_name('.*py$')


def word_vs_pkgs_regex_stats(regex):
    words, pkgs, pkgs_words = words_and_pkg_names_satisfying_regex(regex)
    return {'words': len(words) / n_words, 'pkgs': len(pkgs) / n_pkgs}


def multiple_word_vs_pkgs_regex_stats(patterns):
    """
    Get proportions of english and pkg names that satisfy a regex pattern
    :param patterns:
    :return:
    """
    if isinstance(patterns, str):
        patterns = [patterns]
    if not isinstance(patterns, dict):
        patterns = {p: p for p in patterns}

    return [dict(pattern=name, **word_vs_pkgs_regex_stats(pattern)) for name, pattern in patterns.items()]


def subsequence_counts(n=2, n_of_top_counts=10):
    """
    Get counts of subsequences of letters in english and pypi pkg words
    :param n:
    :param n_of_top_counts:
    :return:
    """
    from collections import Counter
    from itertools import islice

    def window(seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    word_subseqs = Counter()
    for w in simple_words:
        word_subseqs.update(window(w, n))

    pkg_subseqs = Counter()
    for w in pkg_names:
        pkg_subseqs.update(window(w, n))

    t = [(''.join(x[0]), x[1]) for x in word_subseqs.most_common(n_of_top_counts)]
    tt = [(''.join(x[0]), x[1]) for x in pkg_subseqs.most_common(n_of_top_counts)]
    return {'words': t, 'pkgs': tt}


if __name__ == '__main__':
    import argh
    from functools import wraps

    parser = argh.ArghParser()


    def mk_postproc_deco(postproc_func, func_rename=None):
        def decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                return postproc_func(func(*args, **kwargs))

            if func_rename is not None:
                wrapped_func.__name__ = func_rename(func)
            return wrapped_func

        return decorator


    column_disp = mk_postproc_deco(lambda x: '\n'.join(x))
    counts = mk_postproc_deco(lambda x: '\n'.join(x))

    funcs = []
    funcs += list(map(column_disp,
                      [words_containing_py_free_for_pkg,
                       words_starting_with_py_free_for_pkg,
                       words_ending_with_py_free_for_pkg]))
    funcs += [multiple_word_vs_pkgs_regex_stats, subsequence_counts]

    parser.add_commands([words_and_pkg_names_satisfying_regex, is_not_a_pkg_name, allwords, pkgnames])
    parser.dispatch()

# print(multiple_word_vs_pkgs_regex_stats({'contains "py"': '.*py.*',
#                                          'starts with py': 'py.*$',
#                                          'ends with py': '.*py$'
#                                          }))
#
# print()
# print(subsequence_counts(n=3))
#
# print(len([w for w in pkg_names if 'django-' in w]))
# print(len(pkg_names))
