__author__ = 'thorwhalen'

import os

rootdir = os.path.dirname(__file__)
ppath = lambda path: os.path.join(rootdir, path)
dpath = lambda path: os.path.join(rootdir, 'data', path)
