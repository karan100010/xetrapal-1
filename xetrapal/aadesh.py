#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  16 00:31:18 2019

@author: arjunvenkatraman
"""


class Aadesh(object):
    def __init__(self):
        self.msg = None
        self.func = None
        self.args = []
        self.kwargs = {}

    def __repr__(self):
        attrs = []
        for name in self.__dict__.keys():
            value = getattr(self, name)
            attrs.append('\n    {} = {!r},'.format(name, value))
        return '\n{}: {}\n'.format(type(self).__name__, ''.join(attrs))
