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
            hostname = bare_metal.hostname
        try:
            ip = IPv4Address(hostname)
        except (AddressValueError, ValueError):
            ip = None

        # try to guess the mac to use
        if "Mac" in bare_metal.__dict__:
            mac = bare_metal.Mac
        else:
            # get all available macs
            macs = []
            for nic in bare_metal.NICs.iteritems():
                if nic[0] != "lo":
                    macs.append(nic[1]["Mac"])

            if len(macs) == 1:
                mac = macs[0]
            elif len(macs) == 0:
                logger.error("cannot Rory install - couldn't determine mac")
                raise RoryError("couldn't determine mac")
            else:
                mac = Utils.locate_mac_in_log(locate_macs=macs)
                if not mac:
                    mac = macs[0]
        url = "http://google.com"
        data = {"profile": profile, "mac": mac}
        if ip is None:
            data["hostname"] = hostname
        else:
            data["ip"] = str(ip)
        data = dumps(data)
        rest_put(url=url, data=data)
        return url, data


class RoryError(Exception):
    pass
