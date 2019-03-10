# coding: utf-8

from . import astra
from . import karma
from . import jeeva
# from . import fbkarmas
# from . import twkarmas
# from . import wakarmas
# from . import gdkarmas
import colored
# from . import twastras
# from . import gdastras
# from . import smsastras
from . import aadesh
from inspect import getmembers, isfunction

# import gdkarmas
from . import pykkakarta
# import os
# import mojomailastras
# from . import telegramastras
# import telegramkarmas
# import thespiankarta


class Xetrapal(jeeva.Jeeva):
    def __init__(self, *args, **kwargs):
        super(Xetrapal, self).__init__(*args, **kwargs)
        self.vaahans = {}
        self.astras = {}
        self.update_astras()
        self.update_vaahans()
        self.save_profile()
        self.load_module(astra)
        self.load_module(karma)

    def update_astras(self):
        self.logger.info("Trying to update astras")
        astras = {}
        if self.astras == {}:
            self.logger.warning("I dont seem to have any astras")
        else:
            for astraname in self.astras.keys():
                astras[astraname] = str(type(self.astras[astraname]))

        self.set_property("astras", astras)
        self.save_profile()

    def update_vaahans(self):
        self.logger.info("Trying to update vaahans")
        vaahans = {}
        if self.vaahans == {}:
            self.logger.warning("I dont seem to have any vaahans")
        else:
            for vaahanname in self.vaahans.keys():
                vaahans[vaahanname] = str(type(self.vaahans[vaahanname]))

        self.set_property("vaahans", vaahans)
        self.save_profile()

    def add_vaahan(self, vaahan):
        self.vaahans[vaahan.name] = vaahan
        self.update_vaahans()

    def release_vaahan(self, vaahanname):
        self.logger.info("Releasing vaahan " + colored.stylize(vaahanname, colored.fg("violet")))
        vaahan = self.vaahans.pop(vaahanname)
        self.update_vaahans()
        return vaahan

    def add_astra(self, astraname, newastra):
        self.astras[astraname] = newastra
        self.update_astras()

    def drop_astra(self, astraname):
        self.logger.info("Dropping astra " + colored.stylize(astraname, colored.fg("violet")))
        droppedastra = self.astras.pop(astraname)
        self.update_astras()
        return droppedastra

    def get_aadesh(self, message):
        if isinstance(message, (aadesh.Aadesh)):
            self.logger.info("Received Aadesh " + str(message))
            if message.msg == "run":
                self.logger.info("Trying to run " + str(message.func))
                # message['kwargs']['logger']=self.jeeva.logger
                try:
                    message.kwargs['logger'] = self.logger
                    message.func(*message.args, **message.kwargs)
                except Exception as e:
                    self.jeeva.logger.error(repr(e))
            if message.msg == "get":
                self.logger.info(
                    "Trying to get a return value from " + str(message.func))
                try:
                    # message.kwargs['logger'] = self.logger
                    returnval = message.func(*message.args, **message.kwargs)
                    self.logger.info("Got value {}".format(returnval))
                    return returnval
                except Exception as e:
                    self.logger.error(repr(e))
                    return repr(e)

    def start_pykka_karta(self):
        kartaref = pykkakarta.Karta.start(jeeva=self)
        self.kartarefs.append(kartaref)
        return kartaref
    '''
    def get_browser(self):
        browser = astra.get_browser(download_dir=self.sessiondownloadpath, logger=self.logger)
        return browser

    def get_fb_browser(self, fbconfig=None):
        if fbconfig is None:
            if "Facebook" in self.config.sections():
                fbconfig = karma.get_section(
                    self.config, "Facebook", logger=self.logger)
                fbbrowser = astra.get_browser(logger=self.logger)
        fbkarmas.fb_login(fbbrowser, fbconfig, logger=self.logger)
        if "fbbrowser" not in self.astras.keys():
            self.add_astra('fbbrowser', fbbrowser)
        return fbbrowser

    def get_twython(self, twconfig=None):
        if twconfig is None:
            if "Twython" in self.config.sections():
                twconfig = karma.get_section(self.config, "Twython")
        tw = twastras.get_twython(twconfig, logger=self.logger)
        twkarmas.twython_check_auth(tw, logger=self.logger)
        tw.verify_credentials()
        if "twython" not in self.astras.keys():
            self.add_astra('twython', tw)
        return tw

    def get_tweepy(self, twconfig=None):
        if twconfig is None:
            if "Twython" in self.config.sections():
                twconfig = karma.get_section(self.config, "Twython")
        tweep = twastras.get_tweepy(twconfig, logger=self.logger)
        if "tweepy" not in self.astras.keys():
            self.add_astra("tweepy", tweep)
        return tweep

    def get_twython_streamer(self, twconfig=None, ofilename=None):
        if twconfig is None:
            if "Twython" in self.config.sections():
                twconfig = karma.get_section(self.config, "Twython")
        if ofilename is None:
            ofilename = os.path.join(self.sessionpath, "TwythonStreamer.json")
        tw = twastras.get_twython_streamer(
            twconfig, ofilename, logger=self.logger)
        if "twythonstreamer" not in self.astras.keys():
            self.add_astra('twythonstreamer', tw)
        return tw

    def get_googledriver(self, gdconfig=None):
        if gdconfig is None:
            if "Pygsheets" in self.config.sections():
                gdconfig = karma.get_section(self.config, "Pygsheets")
            else:
                self.logger.error("Pyugsheets config missing")
                return None
        gd = gdastras.get_googledriver(gdconfig, logger=self.logger)
        if "pygsheet" not in self.astras.keys():
            self.add_astra('pygsheet', gd)
        return gd

    def get_sms_astra(self, smsconfig=None):
        if smsconfig is None:
            if "SMSAstra" in self.config.sections():
                smsconfig = karma.get_section(self.config, "SMSAstra")
            else:
                self.logger.error("SMSAstra config section missing")
                return None
        sms = smsastras.get_sms_astra(smsconfig, self.logger)
        if "sms" not in self.astras.keys():
            self.add_astra("sms", sms)
        return sms

    def post_tweet(self, tweet):
        tweetmsg = karma.get_aadesh(
            'run', self.astras['twython'].update_status, kwargs={'status': tweet})
        if self.kartarefs == []:
            tweetkarta = self.start_pykka_karta()
        else:
            tweetkarta = self.kartarefs[0]
        tweetkarta.tell(tweetmsg)

    def get_tg_bot(self):
        tg_bot = telegramastras.XetrapalTelegramBot(
            self.config, logger=self.logger)
        if tg_bot.name not in self.astras.keys():
            self.add_astra(tg_bot.name, tg_bot)
        return tg_bot
    '''

    def load_func(self, func):
        def call(*args, **kwargs):
            args = list(args)
            kwargs['logger'] = self.logger
            kwargs['path'] = self.sessiondownloadpath
            kwargs['config'] = self.config
            # print(args, kwargs)
            return func(*args, **kwargs)
        return call

    def load_module(self, module):
        functions_list = [o for o in getmembers(module) if isfunction(o[1])]
        for func in functions_list:
            self.__dict__[func[0]] = self.load_func(func[1])
