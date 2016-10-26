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
from logging import getLogger

from Luke.OSCommitters.DHCPCommitter import OSCommitter

logger = getLogger(__name__)


class CleanCommitter(OSCommitter):
    def __init__(self):
        OSCommitter.__init__(self)

    def commit(self, bare_metal, request):
        ret_value = True
        bare_metal.__dict__['status'] = "matched"
        bare_metal.__dict__['action'] = "run"
        if "image" in request.other_prop:
            bare_metal.__dict__["image_url"] = request.other_prop["image"]["url"]
        elif self.parser.has_section(request.os):
            bare_metal.__dict__["image_url"] = self.parser.get(request.os, "url")
        else:
            logger.warn("could not resolve url from bm {}, request {}".format(bare_metal.id, request.id))
            ret_value = False
        return ret_value
