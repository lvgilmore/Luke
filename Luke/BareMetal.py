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

from json import loads
from logging import getLogger
from uuid import uuid4

from Luke.common.Status import Status
from .utils.Utils import locate_mac_in_log

logger = getLogger(__name__)


class BareMetal(object):
    def __init__(self, bare_metal_str, bm_id=None, hostname=None, ip=None, mac=None):
        self.status = Status.nothing

        # load everything from the string
        json_bare = loads(bare_metal_str)
        for key, value in json_bare.iteritems():
            self.__dict__[key] = value

        # if bm_id:
        #     self.id = bm_id
        self.id = bm_id if bm_id else str(uuid4())
        self.ip = ip if ip else self._init_ip(json_bare=json_bare)
        self.mac = mac if mac else self._init_mac(json_bare=json_bare)
        self.hostname = hostname if hostname else self._init_hostname(json_bare=json_bare)

    def _init_ip(self, json_bare):
        # guess ip
        self.ip = None
        if 'ip' in json_bare:
            self.ip = json_bare['ip']
        elif 'NICs' in json_bare:
            ips = []
            for nic in json_bare['NICs'].itervalues():
                if 'ip' in nic and nic['ip'] != '127.0.0.1':
                    ips.append(nic['ip'])
            if len(ips):
                self.ip = ips[0]

        if not self.ip:
            logger.error("couldn't determine ip for BareMetal {}".format(str(self)))

        return self.ip

    def _init_mac(self, json_bare):
        # guess mac
        self.mac = None
        macs = []
        if 'Mac' in json_bare:
            self.mac = json_bare['mac']
        elif 'NICs' in json_bare:
            for nic in json_bare['NICs'].itervalues():
                if 'Mac' in nic:
                    macs.append(nic['Mac'])
                    if 'ip' in nic and nic['ip'] == self.ip:
                        self.mac = nic['Mac']
        if not self.mac:
            if len(macs) == 1:
                self.mac = macs[0]
            elif len(macs) == 0:
                logger.error("cannot determine mac for BareMetal {}".format(str(self)))
            else:
                self.mac = locate_mac_in_log(search_macs=macs)
                if not self.mac:
                    self.mac = macs[0]
        return self.mac

    def _init_hostname(self, json_bare):
        # guess hostname
        if 'hostname' in json_bare:
            self.hostname = json_bare['hostname']
        elif self.ip:
            self.hostname = self.ip
        else:
            self.hostname = None
        return self.hostname


if __name__ == "__main__":
    pass
