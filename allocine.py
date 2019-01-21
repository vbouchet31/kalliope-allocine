# -*- coding: utf-8 -*-
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from base64 import b64encode
from urllib import urlencode
import hashlib
import json
import datetime
import requests
import time


ALLOCINE_BASE_URL = "http://api.allocine.fr/rest/v3/"
ALLOCINE_PARTNER_KEY = '100043982026'
ALLOCINE_SECRET_KEY = '29d185d98c984a359e6e6f26a0474269'
ANDROID_USER_AGENT = 'Dalvik/1.6.0 (Linux; U; Android 4.2.2; Nexus 4 Build/JDQ39E)'


class Allocine(NeuronModule):
    def __init__(self, **kwargs):
        super(Allocine, self).__init__(**kwargs)

        self.say({"Init Allocine"})
        # the args from the neuron configuration
        self.option = kwargs.get('option', None)

        # Validate the option argument.
        if self.option is None:
            raise MissingParameterException('[Allocine] You need to set a valid option.')
        else:
            options = ['getShowTimesList']
            if self.option not in options:
                raise MissingParameterException('[Allocine] %s is not a valid option.' % self.option)

        self.theater = kwargs.get('theater', None)

        # Validate theater is provided for getShowTimesList option.
        if self.option == "getShowTimesList":
            if self.theater is None:
                raise MissingParameterException('[Allocine] You need to provide a theater code.')
            else:
                events = self.showTimeList(self.theater)
                self.say({'events': events})

    def doRequest(self, method, params):
        sed = time.strftime("%Y%m%d")
        sha1 = hashlib.sha1()
        PARAMETER_STRING = "partner=" + ALLOCINE_PARTNER_KEY + "&" + "&".join(
            [k + "=" + params[k] for k in params.keys()]) + "&sed=" + sed
        SIG_STRING = bytes(ALLOCINE_SECRET_KEY + PARAMETER_STRING).encode('utf-8')
        sha1.update(SIG_STRING)
        SIG_SHA1 = sha1.digest()
        SIG_B64 = b64encode(SIG_SHA1).decode('utf-8')
        sig = urlencode({SIG_B64: ''})[:-1]
        URL = ALLOCINE_BASE_URL + method + "?" + PARAMETER_STRING + "&sig=" + sig
        headers = {'User-Agent': ANDROID_USER_AGENT}
        results = requests.get(URL, headers=headers).text
        try:
            return json.loads(results)
        except Exception as e:
            return results

    # Get today shows time in given theater.
    def showTimeList(self, theater):
        data = {"format": "json", "theaters": theater, "date": datetime.datetime.now().strftime("%Y-%m-%d")}
        items = self.doRequest("showtimelist", data)

        events = dict()
        for key, value in enumerate(items["feed"]["theaterShowtimes"][0]["movieShowtimes"]):
            if not events.get(value["onShow"]["movie"]["code"]):
                events[value["onShow"]["movie"]["code"]] = dict()
                events[value["onShow"]["movie"]["code"]]["name"] = value["onShow"]["movie"]["title"]

            if not events[value["onShow"]["movie"]["code"]].get("times"):
                events[value["onShow"]["movie"]["code"]]["times"] = list()

            # TODO: Order the times.
            for times in value["scr"][0]["t"]:
                events[value["onShow"]["movie"]["code"]]["times"].append(times["$"])

        return events
