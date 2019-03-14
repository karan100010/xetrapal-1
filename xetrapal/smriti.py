#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2019-01-09

@author: arjunvenkatraman
"""

from mongoengine import Document, fields, DynamicDocument
import datetime
from flask_mongoengine import QuerySet
from . import aadhaar
# from samvad import utils
import json
import bson


class PPrintMixin(object):
    def __str__(self):
        return '{}: id={!r}'.format(type(self).__name__, self.id)

    def __repr__(self):
        attrs = []
        for name in self._fields.keys():
            value = getattr(self, name)
            if isinstance(value, (Document, DynamicDocument)):
                attrs.append('\n    {} = {!s},'.format(name, value))
            elif isinstance(value, (datetime.datetime)):
                attrs.append('\n    {} = {},'.format(
                    name, aadhaar.get_local_ts(value).strftime("%Y-%m-%d %H:%M:%S")))
            else:
                attrs.append('\n    {} = {!r},'.format(name, value))
        if self._dynamic_fields:
            for name in self._dynamic_fields.keys():
                value = getattr(self, name)
                if isinstance(value, (Document, DynamicDocument)):
                    attrs.append('\n    {} = {!s},'.format(name, value))
                elif isinstance(value, (datetime.datetime)):
                    attrs.append('\n    {} = {},'.format(
                        name, aadhaar.get_local_ts(value).strftime("%Y-%m-%d %H:%M:%S")))
                else:
                    attrs.append('\n    {} = {!r},'.format(name, value))
        return '\n{}: {}\n'.format(type(self).__name__, ''.join(attrs))


class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class SmritiBase(PPrintMixin):
    observed_timestamp = fields.DateTimeField(default=datetime.datetime.utcnow, required=True)
    updated_timestamp = fields.DateTimeField(default=datetime.datetime.utcnow, required=True)
    created_timestamp = fields.DateTimeField()
    naam = fields.StringField(unique=True, required=False, sparse=True)

    def save(self, *args, **kwargs):
        self.updated_timestamp = datetime.datetime.utcnow()
        super(SmritiBase, self).save(*args, **kwargs)


class XetrapalSmriti(SmritiBase, DynamicDocument):
    configfile = fields.StringField(unique=True, required=False, sparse=True)
    lastsession = fields.ReferenceField('XetrapalSession')
    meta = {"queryset_class": CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['lastsession'] = json.loads(self.lastsession.to_json())
        return bson.json_util.dumps(data)


class XetrapalSession(SmritiBase, DynamicDocument):
    session_name = fields.StringField(unique=True, required=True)
    source_smriti = fields.ReferenceField(XetrapalSmriti)
    functions_loaded = fields.ListField(default=[])
    sessionurlbase = fields.StringField()
