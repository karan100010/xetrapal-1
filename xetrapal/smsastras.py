#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 13:41:18 2019

@author: arjunvenkatraman
"""
from urllib.request import Request, urlopen
import json
from . import astra

payload = {"message": "", "recipients": []}
recipient = {"type": "mobile", "value": ""}


class XPalFrontlineSMS(object):
    def __init__(self, config, logger=astra.baselogger):
        self.logger = logger
        self.logger.info("Setting up FrontlineSMS")
        self.url = config.get("SMSAstra", "apiurl")
        try:
            with open(config.get("SMSAstra", "apikeyfile"), "rb") as f:
                self.apikey = f.read().strip()
        except Exception as e:
            self.logger.error("Error setting up FLSMS {}".format(str(e)))

    def send_sms(self, smsdict):
        if smsdict.keys() != payload.keys():
            self.logger.error("Payload keys do not match")
        data = {}
        data['apiKey'] = self.apikey
        data['payload'] = smsdict
        req = Request(self.url)
        req.add_header('Content-Type', 'application/json')
        try:
            response = json.loads(urlopen(req, json.dumps(data)).read())
            if response['message'] == "success":
                self.logger.info("Got response {}".format(response))
            else:
                self.logger.error("Got response {}".format(response))
            return response
        except Exception as e:
            self.logger.error("Error sending SMS {}".format(str(e)))


class XPalSMSTester(object):
    def __init__(self, config, logger=astra.baselogger):
        self.logger = logger

    def send_sms(self, smsdict):
        if smsdict.keys() != payload.keys():
            self.logger.error("Payload keys do not match")
        for recipient in smsdict['recipients']:
            self.logger.info("Sent Mock SMS {} to {}".format(smsdict['message'], recipient))


def get_sms_astra(config, logger=astra.baselogger):
        service = config.get("SMSAstra", "service")
        if service == "flsms":
            logger.info("Service is FLSMS")
            try:
                sms = XPalFrontlineSMS(config, logger)
                return sms
            except Exception as e:
                logger.error("Error {}".format(str(e)))
        if service == "tester":
            logger.info("Service is Tester")
            try:
                sms = XPalSMSTester(config, logger)
                return sms
            except Exception as e:
                logger.error("Error {}".format(str(e)))
