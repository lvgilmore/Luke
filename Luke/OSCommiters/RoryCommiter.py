#! /usr/bin/python2.7

"""
Module to prepare Rory for Linux installation
@author: Geiger
@created: 11/09/2016
"""

from ipaddr import AddressValueError
from ipaddr import IPv4Address
from logging import getLogger
from requests import put as rest_put
from json import dumps

from Luke.OSCommiters.ICommiter import ICommiter
from Luke.utils.Utils import Utils

logger = getLogger(__name__)


class RoryCommiter(ICommiter):
    def __init__(self):
        pass

    def commit(self, bare_metal, request):
        profile = request.other_prop["profile"]
        if "hostname" in request.other_prop:
            hostname = request.other_prop["hostname"]
        else:
            hostname = bare_metal.values()[0]["hostname"]
        try:
            ip = IPv4Address(hostname)
        except (AddressValueError, ValueError):
            ip = None

        # try to guess the mac to use
        if "Mac" in bare_metal:
            mac = bare_metal["Mac"]
        else:
            # get all available macs
            macs = []
            for nic in bare_metal.values()[0]["NICs"].values():
                if nic[0] != "lo":
                    macs.append(nic[1]["Mac"])

            if len(macs) == 1:
                mac = macs[0]
            elif len(macs) == 0:
                logger.error("cannot Rory install - couldn't determine mac")
                raise RoryError("couldn't determine mac")
            else:
                mac = Utils._locate_mac_in_log(locate_macs=macs)
                if not mac:
                    mac = macs[0]
        url = "http://google.com"
        data = {"profile": profile, "mac": mac}
        if ip is None:
            data["hostname"] = hostname
        else:
            data["ip"] = ip
        data = dumps(data)
        rest_put(url=url, data=data)


class RoryError(Exception):
    pass
