#! /usr/bin/python2.7

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Commits the decision of the MatchMaker at the DHCP level
This module manipulates the DHCP configuration file
@author: Geiger
@created: 11/09/2016
"""

import os
from ConfigParser import ConfigParser
from logging import getLogger
from random import uniform
from socket import gethostbyaddr
from socket import herror

from ipaddr import IPv4Address
from ipaddr import IPv4Network

from Luke.BareMetal import BareMetal
from Luke.OSCommiters.ICommiter import ICommiter
from Luke.Request import Request
from Luke.utils.DHCPConfParser import load as dhcp_load
from Luke.utils.DHCPConfParser import save as dhcp_save
from Luke.utils.Utils import Utils

logger = getLogger(__name__)
SECTION = 'SECTION'


class DHCPCommiter(ICommiter):
    def __init__(self, dhcp_file=None):
        self.parser = ConfigParser()
        if os.environ['LUKE_PATH'] == "":
            os.environ['LUKE_PATH'] = os.path.dirname(__file__)
        self.parser.read(os.path.join(os.environ['LUKE_PATH'], 'resources/config.conf'))
        # self.dhcp_config_file = self.parser.get(SECTION, 'DHCP_CONF_FILE')
        if dhcp_file is None:
            self.dhcp_config_file = self.parser.get(SECTION, 'DHCP_CONF_FILE')
        else:
            self.dhcp_config_file = dhcp_file

    def commit(self, bare_metal, request):
        bare_metal = DHCPCommiter._build_host(bare_metal)
        request = self._build_os(request)
        if self._lock_dhcp():
            dhcp_conf = DHCPConfs(dhcp_load(self.dhcp_config_file))
            dhcp_conf.add_host(subnet=bare_metal["subnet"],
                               host=DHCPCommiter._build_dhcp_host(bare_metal,
                                                                  request))
            dhcp_save(configurations=dhcp_conf,
                      conf_file=self.dhcp_config_file)
        else:
            logger.error("couldn't get lock on dhcp. very sad. tears")
        self._release_dhcp()

    @staticmethod
    def _build_host(host):
        """this methods takes unstructured host dictionary and makes it structured

        :param host: unstructured host
        :type host: dict
        :return: structured host
        :rtype: dict
        """
        if isinstance(host, dict):
            pass
        elif isinstance(host, str):
            host = BareMetal(host).__dict__
        elif isinstance(host, BareMetal):
            host = host.__dict__

        if "hostname" in host:
            pass
        elif len(host.keys()) == 1 and isinstance(host.values()[0], dict):
            key = host.keys()[0]
            host = host.values()[0]
            host["hostname"] = key
        elif "ip" in host:
            try:
                host["hostname"] = gethostbyaddr(str(host["ip"]))
            except herror:
                host["hostname"] = str(host["ip"])
        else:
            logger.error("couldn't determine hostname for host "
                         "{}".format(str(host)))
            return False
        if "subnet" not in host:
            if "ip" in host:
                host["subnet"] = Utils.ip_to_subnet(host["ip"])
            else:
                logger.debug(
                    "DHCPCommiter.commit was called without IP nor segment")
        return host

    def _build_os(self, request):
        """like _build_host, but for os

        :param host: unstructured os and related info
        :type host: dict
        :return: structured os and related info
        :rtype: dict
        """
        if isinstance(request, dict):
            pass
        elif isinstance(request, str):
            request = Request(request).__dict__
        elif isinstance(request, Request):
            request = request.__dict__

        if "next server" not in request:
            request["next-server"] = self.parser.get(request['os'], 'NEXT_SERVER')
        if "filename" not in request:
            request["filename"] = self.parser.get(request['os'], 'TFTP_FILENAME')
        return request

    @staticmethod
    def _build_dhcp_host(host, os):
        hostname = host["hostname"]
        dhcp_host = {hostname: {"options": {}}}
        dhcp_host[hostname]["options"]["hardware"] = []
        dhcp_host[hostname]["options"]["fixed-address"] = []
        if "ip" in host:
            dhcp_host[hostname]["options"]["fixed-address"].append(host["ip"])
        for key, nic in host["NICs"].iteritems():
            dhcp_host[hostname]["options"]["hardware"].append(
                "ethernet " + str(nic["Mac"]))
            if "ip" in nic:
                dhcp_host[hostname]["options"]["fixed-address"].append(
                    nic["ip"])
        dhcp_host[hostname]["options"]["next-server"] = os["next-server"]
        dhcp_host[hostname]["options"]["filename"] = os["filename"]
        return dhcp_host

    def _lock_dhcp(self):
        lock_file = self.dhcp_config_file + ".lock"
        locker = {"pid": 0, "count": 0}
        pid = os.getpid()
        for i in range(0, 10):
            try:
                f = open(lock_file, 'r')
                f.close()
                locker = self._check_deadlock(locker=locker,
                                              lock_file=lock_file)
                os.system("sleep {}".format(uniform(0, 1)))
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
            if os.system("ps -ef | grep ' {} ' | grep -vq grep".format(
                    str(current))) == 0:
                logger.warning(
                    "attempting to kill {}. it holds lock for too long".format(
                        str(current)))
                os.kill(int(current), 15)
            else:
                logger.info(
                    "process {} locking dhcp but seems dead."
                    " deleting the lock file".format(str(current)))
                os.remove(lock_file)
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
        pid = os.getpid()
        if self._check_lock(lock_file=lock_file, current=pid):
            os.remove(lock_file)
        else:
            logger.critical("_release_dhcp was called for process {}, "
                            "but I don't hold the lock!".format(pid))
            raise LockError("_release_dhcp was called for process {}, "
                            "but I don't hold the lock!".format(pid))


class DHCPConfs(object):
    def __init__(self, confs=None):
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
            self.shared_nets = confs["shared_networks"]

    def add_host(self, subnet, host):
        path = self._find_host(host=host)
        if path:
            logger.info("add_host {} requested, but already in file".format(
                host))
            path.pop(host.keys()[0])
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
        """finds if a subnet is defined in an object, if so returns it

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

    def _find_host(self, host, scope=None):
        """like _find_subnet, but for hosts

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
        if "hosts" in scope and host.keys()[0] in scope["hosts"]:
            return scope["hosts"]
        for i in scope.values():
            path = self._find_subnet(host, i)
            if path:
                return path
        return False


class LockError(Exception):
    pass

if __name__ == "__main__":
    dhc = DHCPCommiter("../resources/dhcp-example.conf")
    dhc.commit(bare_metal={"subnet": IPv4Network("192.168.0.1/24"),
                           "ip": IPv4Address("192.168.0.3"),
                           "NICs": {"eth0": {"Mac": "00:11:22:33:44:66",
                                             "Speed": 100}
                                    }
                           },
               request={})
