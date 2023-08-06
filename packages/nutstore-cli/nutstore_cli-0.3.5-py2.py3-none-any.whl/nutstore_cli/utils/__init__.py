# coding: utf-8
from __future__ import absolute_import

import tempfile


def to_file(s, dest=None):
    dest = dest or tempfile.mktemp(suffix='.log')
    with open(dest, 'w') as g:
        g.write(s)
    return dest
