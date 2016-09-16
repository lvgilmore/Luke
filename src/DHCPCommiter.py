#! /usr/bin/python2.7

"""
Commits the decision of the MatchMaker at the DHCP level
This module manipulates the DHCP configuration file
@author: Geiger
@created: 11/09/2016
"""

from ipaddr import IPv4Network
from logging import getLogger

from src.OSCommiters.ICommiter import ICommiter
from src.utils.DHCPConfParser import load as dhcp_load
from src.utils.DHCPConfParser import save as dhcp_save
from src.utils.Utils import Utils
from src.utils.config import *


class DHCPCommiter(ICommiter):
    def __init__(self):
        self.dhcp_config_file = DHCP_CONF_FILE
        self.logger = getLogger(__name__)

    def commit(self, bare_metal, request):
        bare_metal = self._build_host(bare_metal)
        request = self._build_os(request)
        self._lock_dhcp()
        dhcp_conf = dhcp_load(self.dhcp_config_file)
        dhcp_conf.add_host(subnet=bare_metal["subnet"],
                           host=DHCPCommiter._build_dhcp_host(bare_metal,
                                                              request))
        dhcp_save(configurations=dhcp_conf, conf_file=self.dhcp_config_file)
        self._release_dhcp()
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
        if host.has_key("ip") and not host.has_key("subnet"):
            host["subnet"] = Utils.ip_to_subnet(host["ip"])
        elif not host.has_key("subnet"):
            self.logger.debug(
                "DHCPCommiter.commit was called without ip nor segment")
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

    @staticmethod
    def _build_dhcp_host(host, os):
        hostname = host["hostname"]
        dhcp_host = {hostname: {}}
        dhcp_host[hostname]["macs"] = []
        dhcp_host[hostname]["fixed-address"] = []
        for nic in host["NICs"].iteritems():
            dhcp_host[hostname]["macs"].append(nic["Mac"])
            dhcp_host[hostname]["fixed-address"].append(nic["IP"])
        dhcp_host[hostname]["next-server"] = os["next-server"]
        dhcp_host[hostname]["filename"] = os["filename"]



class DHCPConfs(object):
    def __init__(self, confs=None):
        """
        :type confs: dict
        :param confs: output of DHCPConfParser.parse()
        """
        if confs is None:
            self.globals = {}
            self.subnets = {}
            self.hosts = {}
            self.groups = {}
            self.shared_nets = {}
        else:
            self.globals = confs["globals"]
            self.subnets = confs["subnets"]
            self.hosts = confs["hosts"]
            self.groups = confs["groups"]
            self.shared_nets = confs["shared_nets"]

    def add_host(self, subnet, host):
        pass