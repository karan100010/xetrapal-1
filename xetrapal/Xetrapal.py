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
        self.functions = []
        self.update_astras()
        self.update_vaahans()
        # self.save_profile()
        self.load_module(astra)
        self.load_module(karma)

    def update_astras(self):
        self.logger.info("Trying to update astras")
        # astras = {}
        if self.astras == {}:
            self.logger.warning("I dont seem to have any astras")
        '''
        else:
            for astraname in self.astras.keys():
                astras[astraname] = str(type(self.astras[astraname]))
        '''
        # self.set_property("astras", astras)
        self.session.astras = self.astras
        for ast in self.session.astras.keys():
            self.session.astras[ast] = str(self.session.astras[ast])
        self.session.save()
        self.session.reload()

    def update_vaahans(self):
        self.logger.info("Trying to update vaahans")
        vaahans = {}
        if self.vaahans == {}:
            self.logger.warning("I dont seem to have any vaahans")
        else:
            for vaahanname in self.vaahans.keys():
                vaahans[vaahanname] = str(type(self.vaahans[vaahanname]))

        # self.set_property("vaahans", vaahans)
        self.session.vaahans = self.vaahans
        self.session.save()
        self.session.reload()
        # self.save_profile()

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

    def load_func(self, func):
        def call(*args, **kwargs):
            args = list(args)
            kwargs['logger'] = self.logger
            kwargs['path'] = self.sessiondownloadpath
            kwargs['config'] = self.configfile
            for key in self.astras.keys():
                kwargs[key] = self.astras[key]
            # print(args, kwargs)
            return func(*args, **kwargs)
        return call

    def load_module(self, module):
        self.logger.info("Trying to load module {}".format(module.__name__))
        try:
            functions_list = [o for o in getmembers(module) if isfunction(o[1])]
            for func in functions_list:
                self.__dict__[func[0]] = self.load_func(func[1])
            self.functions += [f[0] for f in functions_list]
            self.functions = list(set(self.functions))
            self.functions.sort()
            self.session.functions_loaded += self.functions
            self.session.functions_loaded = list(set(self.session.functions_loaded))
            self.session.save()
            self.session.reload()
            self.logger.info("I now have functions {}".format(self.functions))
        except Exception as e:
            self.logger.error("Error loading module {}, {} {}".format(module.__name__, type(e), str(e)))
