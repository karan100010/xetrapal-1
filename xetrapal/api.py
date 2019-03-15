"""
Created on Sat Sep 22 20:54:42 2018

@author: arjun
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
# from flask_mongoengine import MongoEngine
import json
# import datetime
from flask_restful import reqparse, Api, Resource
from flask_mongoengine import MongoEngine
# import urllib
from . import smriti, Xetrapal, wakarmas, wasmriti
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

me = MongoEngine(app)
# me = MongoEngine(app)
# app.logger = xpal.samvadxpal.logger

api = Api(app)
parser = reqparse.RequestParser()

apismriti = smriti.XetrapalSmriti.objects(naam="xpal-api")[0]
apixpal = Xetrapal(apismriti)
apixpal.dhaarana(wakarmas)


def ujsonify(dictionary, logger=apixpal.logger):
    logger.info("Trying to jsonify dictionary {}".format(dictionary))
    if "resp" not in dictionary.keys() or "status" not in dictionary.keys():
        return jsonify({"resp": "error Jsonifying", "status": "error"})
    else:
        resp = dictionary['resp']
        status = dictionary['status']
        if type(resp) == list:
            for response in resp:
                if hasattr(response, "files"):
                    logger.info("Adding urls")
                    response.urls = [x.replace(apixpal.datapath, apixpal.urlbase) for x in response['files']]
                    response.save()
        return jsonify({"resp": resp, "status": status})


class ApiResource(Resource):
    def get(self, command=None):
        status = "success"
        try:
            if command is None:
                resp = ["API Running" + repr(apixpal.smriti)]
            elif command == "api_profile":
                resp = [json.loads(apixpal.smriti.to_json())]
            elif command == "smriti_status":
                resp = [apixpal.get_smriti_status()]
            else:
                resp = "error: Unrecognized command"
                status = "error"
        except Exception as e:
                resp = "error: {} {}".format(type(e), str(e))
                status = "error"
        return ujsonify({"resp": resp, "status": status})


api.add_resource(ApiResource, "/", endpoint="api-root")
api.add_resource(ApiResource, "/<string:command>", endpoint="api-command")


class XetrapalSessionResource(Resource):
    def get(self, session_id=None, session_name=None):
        status = "success"
        resp = []
        try:
            apixpal.session.save()
            apixpal.smriti.reload()
            apixpal.session.reload()
            apixpal.smriti.lastsession.reload()
            if session_id is not None:
                resp = [smriti.XetrapalSession.objects.with_id(session_id)]
            elif session_name is not None:
                resp = smriti.XetrapalSession.objects(session_name=session_name)
            else:
                resp = smriti.XetrapalSession.objects()
        except Exception as e:
                resp = "error: {} {}".format(type(e), str(e))
                status = "error"
        return ujsonify({"resp": resp, "status": status})


api.add_resource(XetrapalSessionResource, "/xetrapal_session", endpoint="xetrapal_session")
api.add_resource(XetrapalSessionResource, "/xetrapal_session/by_id/<string:session_id>", endpoint="xetrapal_session_id")
api.add_resource(XetrapalSessionResource, "/xetrapal_session/by_name/<string:session_name>", endpoint="xetrapal_session_name")


class XetrapalSmritiResource(Resource):
    def get(self, smriti_id=None, name=None):
        status = "success"
        resp = []
        try:
            apixpal.session.save()
            apixpal.smriti.reload()
            apixpal.session.reload()
            apixpal.smriti.lastsession.reload()
            if smriti_id is not None:
                resp = [smriti.XetrapalSmriti.objects.with_id(smriti_id)]
            elif name is not None:
                resp = smriti.XetrapalSmriti.objects(name=name)
            else:
                resp = smriti.XetrapalSmriti.objects()
        except Exception as e:
                resp = "error: {} {}".format(type(e), str(e))
                status = "error"
        return ujsonify({"resp": resp, "status": status})


api.add_resource(XetrapalSmritiResource, "/xetrapal_smriti", endpoint="xetrapal_smriti")
api.add_resource(XetrapalSmritiResource, "/xetrapal_smriti/by_id/<string:smriti_id>", endpoint="xetrapal_smriti_id")
api.add_resource(XetrapalSmritiResource, "/xetrapal_smriti/by_name/<string:name>", endpoint="xetrapal_smriti_name")


class WhatsappConversationResource(Resource):
    def get(self, waconv_id=None, display_name=None):
        status = "success"
        resp = []
        try:
            apixpal.session.save()
            apixpal.smriti.reload()
            apixpal.session.reload()
            apixpal.smriti.lastsession.reload()
            if waconv_id is not None:
                resp = [wasmriti.WhatsappConversation.objects.with_id(waconv_id)]
            elif display_name is not None:
                resp = wasmriti.WhatsappConversation.objects(display_name=display_name)
            else:
                resp = wasmriti.WhatsappConversation.objects()
        except Exception as e:
                resp = "error: {} {}".format(type(e), str(e))
                status = "error"
        return ujsonify({"resp": resp, "status": status})


api.add_resource(WhatsappConversationResource, "/whatsapp_conversation", endpoint="whatsapp_conversation")
api.add_resource(WhatsappConversationResource, "/whatsapp_conversation/by_id/<string:waconv_id>", endpoint="whatsapp_conversation_id")
api.add_resource(WhatsappConversationResource, "/whatsapp_conversation/by_name/<string:display_name>", endpoint="whatsapp_conversation_name")


class WhatsappMessageResource(Resource):
    def get(self, wamsg_id=None):
        status = "success"
        resp = []
        try:
            apixpal.session.save()
            apixpal.smriti.reload()
            apixpal.session.reload()
            apixpal.smriti.lastsession.reload()
            if wamsg_id is not None:
                resp = [wasmriti.WhatsappMessage.objects.with_id(wamsg_id)]
            else:
                resp = list(wasmriti.WhatsappMessage.objects())
        except Exception as e:
                resp = "error: {} {}".format(type(e), str(e))
                status = "error"
        return ujsonify({"resp": resp, "status": status})


api.add_resource(WhatsappMessageResource, "/whatsapp_message", endpoint="whatsapp_message")
api.add_resource(WhatsappMessageResource, "/whatsapp_message/by_id/<string:wamsg_id>", endpoint="whatsapp_message_id")
# api.add_resource(WhatsappMessageResource, "/whatsapp_message/by_name/<string:display_name>", endpoint="whatsapp_message_name")


class WhatsappProfileResource(Resource):
    def get(self, waprof_id=None, naam=None):
        status = "success"
        resp = []
        try:
            apixpal.session.save()
            apixpal.smriti.reload()
            apixpal.session.reload()
            apixpal.smriti.lastsession.reload()
            if waprof_id is not None:
                resp = [wasmriti.WhatsappProfile.objects.with_id(waprof_id)]
            elif naam is not None:
                resp = list(wasmriti.WhatsappProfile.objects(naam=naam))
            else:
                resp = list(wasmriti.WhatsappProfile.objects())
        except Exception as e:
                resp = "error: {} {}".format(type(e), str(e))
                status = "error"
        return ujsonify({"resp": resp, "status": status})


api.add_resource(WhatsappProfileResource, "/whatsapp_profile", endpoint="whatsapp_profile")
api.add_resource(WhatsappProfileResource, "/whatsapp_profile/by_id/<string:waprof_id>", endpoint="whatsapp_profile_id")
api.add_resource(WhatsappProfileResource, "/whatsapp_profile/by_name/<string:naam>", endpoint="whatsapp_profile_naam")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
