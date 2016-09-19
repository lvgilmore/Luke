#! /usr/bin/python2.7

"""
Commits the decision of the MatchMaker at the DHCP level
This module manipulates the DHCP configuration file
@author: Geiger
@created: 11/09/2016
"""

from ipaddr import IPv4Network, IPv4Address
from logging import getLogger
from os import getpid
from os import kill
from os import remove
from os import system
from random import uniform
from socket import gethostbyaddr
from socket import herror

from src.OSCommiters.ICommiter import ICommiter
from src.utils.DHCPConfParser import load as dhcp_load
from src.utils.DHCPConfParser import save as dhcp_save
from src.utils.Utils import Utils
from src.utils.config import *

logger = getLogger(__name__)


class DHCPCommiter(ICommiter):
    def __init__(self, dhcp_config_file=DHCP_CONF_FILE):
        self.dhcp_config_file = dhcp_config_file

    def commit(self, bare_metal, request):
        bare_metal = DHCPCommiter._build_host(bare_metal)
        request = DHCPCommiter._build_os(request)
        if self._lock_dhcp():
            dhcp_conf = DHCPConfs(dhcp_load(self.dhcp_config_file))
            dhcp_conf.add_host(subnet=bare_metal["subnet"],
                               host=DHCPCommiter._build_dhcp_host(bare_metal,
                                                                  request))
            dhcp_save(configurations=dhcp_conf, conf_file=self.dhcp_config_file)
        else:
            logger.error("couldn't get lock on dhcp. very sad. tears")
        self._release_dhcp()

    @staticmethod
    def _build_host(host):
        """
        this methods takes unstructured host dictionary
        and makes it structured
        :param host: unstructured host
        :type host: dict
        :return: structured host
        :rtype: dict
        """
        if "hostname" in host:
            pass
        elif len(host.keys()) == 1 and isinstance(host.values()[0], dict):
            key = host.keys()[0]
            host = host.values()[0]
            host["hostname"] = key
        elif "IP" in host:
            try:
                host["hostname"] = gethostbyaddr(str(host["IP"]))
            except herror:
                host["hostname"] = str(host["IP"])
        else:
            logger.error("couldn't determine hostname for host "
                         "{}".format(str(host)))
            return False
        if "subnet" not in host:
            if "IP" in host:
                host["subnet"] = Utils.ip_to_subnet(host["IP"])
            else:
                logger.debug(
                    "DHCPCommiter.commit was called without IP nor segment")
        return host

    @staticmethod
    def _build_os(os):
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
            os["next-server"] = NEXT_SERVER
        if not os.has_key("filename"):
            os["filename"] = TFTP_FILENAME
        return os

    @staticmethod
    def _build_dhcp_host(host, os):
        hostname = host["hostname"]
        dhcp_host = {hostname: {"options": {}}}
        dhcp_host[hostname]["options"]["hardware"] = []
        dhcp_host[hostname]["options"]["fixed-address"] = []
        if "IP" in host:
            dhcp_host[hostname]["options"]["fixed-address"].append(host["IP"])
        for key, nic in host["NICs"].iteritems():
            dhcp_host[hostname]["options"]["hardware"].append(
                "ethernet " + str(nic["Mac"]))
            if "IP" in nic:
                dhcp_host[hostname]["options"]["fixed-address"].append(nic["IP"])
        dhcp_host[hostname]["options"]["next-server"] = os["next-server"]
        dhcp_host[hostname]["options"]["filename"] = os["filename"]
        return dhcp_host

    def _lock_dhcp(self):
        lock_file = self.dhcp_config_file + ".lock"
        locker = {"pid": 0, "count": 0}
        pid = getpid()
        for i in range(0, 10):
            try:
                f = open(lock_file, 'r')
                f.close()
                locker = self._check_deadlock(locker=locker, lock_file=lock_file)
                system("sleep {}".format(uniform(0, 1)))
            except IOError:
                # lock DHCP
                f = open(lock_file, 'w')
                f.write(str(pid))
                f.close()
                # check lock
                return self._check_lock(lock_file=lock_file, current=pid)
        return False

    def _check_deadlock(self, locker, lock_file):
        current = Utils.open_read_close(lock_file)
        if current == locker["pid"]:
            locker["count"] += 1
        else:
            locker = {"pid": current,
                      "count": 0}
        if locker["count"] > 3:
            if system("ps -ef | grep ' {} ' | grep -vq grep".format(
                    str(current))) == 0:
                logger.warning(
                    "attempting to kill {}. it holds lock for too long".format(
                        str(current)))
                kill(int(current), 15)
            else:
                logger.info(
                    "process {} locking dhcp but seems dead."
                    " deleting the lock file".format(str(current)))
                remove(lock_file)
        return locker

    def _check_lock(self, lock_file, current):
        temp = Utils.open_read_close(lock_file)
        if int(temp) == int(current):
            return True
        else:
            logger.critical("lock failed miserably")
            raise LockError("lock failed miserably")

    def _release_dhcp(self):
        lock_file = self.dhcp_config_file + ".lock"
        pid = getpid()
        if self._check_lock(lock_file=lock_file, current=pid):
            remove(lock_file)
        else:
            logger.critical("_release_dhcp was called for process {}, "
                            "but I don't hold the lock!".format(pid))
            raise LockError("_release_dhcp was called for process {}, "
                            "but I don't hold the lock!".format(pid))


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
        path = self._find_subnet(subnet=subnet)
        if len(host) != 1:
            raise TypeError
        k, v = host.popitem()
        if path:
            path[subnet]["hosts"][k] = v
        else:
            logger.warning("subnet {} requested but not found".format(
                str(subnet)))
            self.hosts[k] = v

    def _find_subnet(self, subnet, scope=None):
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
        if scope is None:
            scope = self.__dict__
        elif not isinstance(scope, dict):
            return False
        if "subnets" in scope and subnet in scope["subnets"]:
            return scope["subnets"]
        for i in scope.values():
            path = self._find_subnet(subnet, i)
            if path:
                return path
        return False


class LockError(Exception):
    pass

if __name__ == "__main__":
    dhc = DHCPCommiter("../resources/dhcp-example.conf")
    dhc.commit(bare_metal={"subnet": IPv4Network("192.168.0.1/24"),
                           "IP": IPv4Address("192.168.0.3"),
                           "NICs": {"eth0": {"Mac": "00:11:22:33:44:55",
                                             "Speed": 100}
                                    }
                           },
               request={})
