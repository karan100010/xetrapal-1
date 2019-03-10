# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:31:18 2018

@author: ananda
"""
from . import astra
import pygsheets
# Get a pygsheet to work with Google sheets


def get_googledriver(config=None, logger=astra.baselogger, **kwargs):
    logger.info("Trying to log into Google drive")
    try:
        gd = pygsheets.authorize(outh_file=config.get("Pygsheets", 'outhfile'),
                                 outh_nonlocal=True, outh_creds_store=config.get("Pygsheets", 'outhstore'))
        return gd
    except Exception as e:
        logger.error("Could not get google driver config because %s" % str(e))
        return None
