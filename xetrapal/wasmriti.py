#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2019-01-09

@author: arjunvenkatraman
"""

from mongoengine import fields, DynamicDocument
# rom . import aadhaar
from . import smriti
# from samvad import utils
# import json
# import bson


class WhatsappProfile(smriti.SmritiBase, DynamicDocument):
    mobile_num = fields.StringField(unique=True, required=False, sparse=True)
    observed_by = fields.StringField()


class WhatsappConversation(smriti.SmritiBase, DynamicDocument):
    display_name = fields.StringField(unique=True, required=False, sparse=True)
    display_lines = fields.ListField()
    observed_by = fields.ReferenceField(WhatsappProfile)


class WhatsappMessage(smriti.SmritiBase, DynamicDocument):
    text_lines = fields.ListField()
    observed_by = fields.ReferenceField(WhatsappProfile)
    observed_in = fields.ReferenceField(WhatsappConversation)
    sent_by = fields.ReferenceField(WhatsappProfile)
