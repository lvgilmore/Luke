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
from utils.Utils import Utils
from utils.config import *


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


class DHCPConfParser:
    """
    help class to pars the dhcpd.conf file
    """

    def __init__(self, conffile=None):
        """
        :param conffile: either a file or a file path
        """
        if isinstance(conffile, file):
            self.conffile = conffile
        elif isinstance(conffile, str):
            self.conffile = open(conffile)
        elif conffile is not None:
            raise TypeError("unexpected type " + str(conffile.__class__))

        self.globals = []
        self.subnets = []
        self.hosts = []
        self.groups = []
        self.shared_nets = []
        self.parse()

    def parse(self):
        confs = self._preformat()
        self._parse_global(confs)

    def _preformat(self):
        raw_conf = split('(\n|\{|\}|;)', self.conffile.read())
        for i in range(0, raw_conf.__len__()):
            raw_conf[i] = sub('#.*$', '', raw_conf[i])
            raw_conf[i] = sub('^\s+', '', raw_conf[i])
        # clean empty entries
        try:
            while True:
                raw_conf.pop(raw_conf.index(''))
        except ValueError:
            pass
        return raw_conf

    def _parse_global(self, confs):
        conf = confs[0]
        assert isinstance(conf, str)
        if conf.startswith('shared-network'):
            self._parse_shared_network(confs)
        elif conf.startswith('subnet'):
            self._parse_subnet(confs)
        elif conf.startswith('host'):
            self._parse_host(confs)
        elif conf.startswith('group'):
            self._parse_group(confs)
        elif conf.startswith('{') or conf.startswith('}'):
            raise ParseError(
                "unexpected word while parsing {}: {}".format(
                    str(self.conffile), conf))
        else:
            self.globals.append(confs.pop(0))
            while confs[0] in ["\n", ";"]:
                confs.pop(0)

    def _parse_shared_network(self, confs):
        assert isinstance(confs[0], str) and conf.startswith("shared-network")
        conf = confs[0]
        conf.split()


class ParseError(SyntaxError):
    def __init__(self, *args, **kwargs):
        SyntaxError.__init__(self, args, kwargs)


if __name__ == "__main__":
    parser = DHCPConfParser(conffile="../resources/dhcp-example.conf")
    parser.parse()
    print parser.globals
    print parser.groups
    print parser.hosts
    print parser.shared_nets
    print parser.subnets
