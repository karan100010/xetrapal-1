#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from mojomailGMail import MojoGMail
"""
Created on Wed Jun  6 00:31:18 2018

@author: ananda
"""
from . import astra
import sys
sys.path.append("/opt/mojomailman/mojomail")


def get_mojogmail(configfile, logger=astra.baselogger):
    logger.info("Getting a GMail driver")
    m = MojoGMail(configfile=configfile, logger=logger)
    return m
