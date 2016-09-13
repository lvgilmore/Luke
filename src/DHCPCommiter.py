#! /usr/bin/python2.7

"""
Commits the decision of the MatchMaker at the DHCP level
This module manipulates the DHCP configuration file
@author: Geiger
@created: 11/09/2016
"""

from logging import getLogger, DEBUG
from re import sub, split
from src.OSCommiters.ICommiter import ICommiter
from src.utils.Utils import Utils
from src.utils.config import *


class DHCPCommiter(ICommiter):
    def __init__(self):
        self.dhcp_config_file = DHCP_CONF_FILE
        self.logger = getLogger(__name__)

    def commit(self, **kwargs):
        # I expect to get something like host and os
        try:
            host = self._build_host(kwargs["host"])
            os = self._build_os(kwargs["os"])
        except KeyError:
            raise KeyError("DHCPCommiter.commit expects host and os kwargs")
        # TODO: the actual part of adding the host configurations to the DHCP file

    def _build_host(self, host):
        """
        this methods takes unstructured host dictionary
        and makes it structured
        :param host: unstructured host
        :type host: dict
        :return: structured host
        :rtype: dict
        """
        assert isinstance(host, dict)
        if host.has_key("ip") and not host.has_key("subnet"):
            host["subnet"] = Utils.ip_to_subnet(host["ip"])
        elif not host.has_key("subnet"):
            self.logger.log(DEBUG, "DHCPCommiter.commit was called without ip nor segment")
        return host

    def _build_os(self, os):
        """
        like _build_host, this methods takes unstructured host dictionary
        and makes it structured
        :param host: unstructured os and related info
        :type host: dict
        :return: structured os and related info
        :rtype: dict
        """
        assert isinstance(os, dict)
        if not os.has_key("next server"):
            os["next server"] = NEXT_SERVER
        if not os.has_key("filename"):
            os["filename"] = TFTP_FILENAME
