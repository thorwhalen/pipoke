def contains_py(w):
    return 'py' in w


def starts_with_py(w):
    return w.startswith('py')


def ends_with_py(w):
    return w.endswith('py')


contains_py_or_pi = '.*(py|pi).*'