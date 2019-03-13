"""
Created on Sat Sep 22 20:54:42 2018

@author: arjun
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
# from flask_mongoengine import MongoEngine
import json
import datetime
from flask_restful import reqparse, Api, Resource

import urllib
from . import smriti, Xetrapal
# from samvad import xpal

app = Flask(__name__)
'''
app.config.update(
    MONGODB_HOST='localhost',
    MONGODB_PORT='27017',
    MONGODB_DB='xetrapal-smriti',
)
'''
CORS(app)
# me = MongoEngine(app)
# app.logger = xpal.samvadxpal.logger

api = Api(app)
parser = reqparse.RequestParser()

apismriti = smriti.XetrapalSmriti.objects(naam="xpal-api")[0]
apixpal = Xetrapal(apismriti)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
