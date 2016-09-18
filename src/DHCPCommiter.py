#! /usr/bin/python2.7

"""
Commits the decision of the MatchMaker at the DHCP level
This module manipulates the DHCP configuration file
@author: Geiger
@created: 11/09/2016
"""

from ipaddr import IPv4Network
from logging import getLogger
from os import getpid
from os import kill
from os import remove
from os import system
from random import uniform

from src.OSCommiters.ICommiter import ICommiter
from src.utils.DHCPConfParser import load as dhcp_load
from src.utils.DHCPConfParser import save as dhcp_save
from src.utils.Utils import Utils
from src.utils.config import *

logger = getLogger(__name__)


class DHCPCommiter(ICommiter):
    def __init__(self):
        self.dhcp_config_file = DHCP_CONF_FILE

    def commit(self, bare_metal, request):
        bare_metal = DHCPCommiter._build_host(bare_metal)
        request = DHCPCommiter._build_os(request)
        self._lock_dhcp()
        dhcp_conf = dhcp_load(self.dhcp_config_file)
        dhcp_conf.add_host(subnet=bare_metal["subnet"],
                           host=DHCPCommiter._build_dhcp_host(bare_metal,
                                                              request))
        dhcp_save(configurations=dhcp_conf, conf_file=self.dhcp_config_file)
        self._release_dhcp()

    @staticmethod
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
            logger.debug(
                "DHCPCommiter.commit was called without ip nor segment")
        return host

    @staticmethod
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

    def _lock_dhcp(self):
        lock_file = self.dhcp_config_file + ".lock"
        locker = {"pid": 0,
                  "count": 0}
        pid = getpid()
        for i in range(0, 10):
            try:
                f = open(lock_file, 'r')
                # check that there's no deadlock
                temp = f.read()
                if temp == locker["pid"]:
                    locker["count"] += 1
                if locker["count"] > 3:
                    if system("ps -ef | grep ' {} ' | grep -vq grep"
                                      .format(str(temp))) == 0:
                        logger.warning("attempting to kill {}. "
                                       "it holds lock for too long"
                                       .format(str(temp)))
                        kill(int(temp))
                    else:
                        logger.info("process {} locking dhcp but seems dead."
                                    "deleting the lock file"
                                    .format(str(temp)))
                        remove(lock_file)
                system("sleep {}".format(uniform(0, 1)))
            except IOError:
                f = open(lock_file, 'w')
                f.write(str(pid))
                f.close()
                f = open(lock_file, 'r')
                temp = f.read()
                if int(temp) == int(pid):
                    return True
                else:
                    logger.critical("lock failed miserably")
                    raise IOError("lock failed miserably")


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

    def _find_subnet(self, subnet, scope=self.__dict__):
        """
        finds if a subnet is defined in an object,
        if so returns it
        :param subnet: the subnet we look for
        :type subnet: IPv4Network
        :param scope: where to look
        :type scope: dict
        :return: path to the subnet
        :rtype: dict
        """
        if "subnets" in scope and subnet in scope["subnets"]:
            return scope["subnets"]
        for i in scope.values():
            path = self._find_subnet(subnet, i)
            if path:
                return path
        return False
