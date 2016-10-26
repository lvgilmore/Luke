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
from logging import getLogger
from json import dumps
from requests import put as rest_put

from .OSCommitter import OSCommitter

logger = getLogger(__name__)


class RoryCommitter(OSCommitter):
    def __init__(self):
        OSCommitter.__init__(self)
        if not self.parser.has_section('Rory'):
            logger.error("no section: Rory")
        elif not self.parser.has_option('Rory', 'RORY_URL'):
            logger.error("no option: RORY_URL in section: Rory")
        else:
            self.url = self.parser.get('Rory', 'RORY_URL')

    def commit(self, bare_metal, request):

        profile = request.other_prop["profile"]
        if "hostname" in request.other_prop:
            hostname = request.other_prop["hostname"]
        else:
            hostname = bare_metal.hostname
        try:
            ip = bare_metal.ip
        except (AddressValueError, ValueError, AttributeError):
            ip = None

        data = {"profile": profile, "mac": bare_metal.mac}
        if not ip:
            data["hostname"] = hostname
        else:
            data["ip"] = str(ip)
        data = dumps(data)
        rest_put(url=self.url, data=data)
        return self.url, data


class RoryError(Exception):
    pass
