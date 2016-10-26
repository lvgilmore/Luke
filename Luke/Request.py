#! /usr/bin/python
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
import datetime
from logging import getLogger

from common import constants

logger = getLogger(__name__)


class Request(object):
    def __init__(self, json_req, req_id=None):
        self.requirements = json_req[constants.REQS] or {}
        self.other_prop = json_req[constants.OTHER_PROP] or {}
        if constants.OS in json_req:
            self.os = json_req[constants.OS]
        else:
            self.os = constants.DEFAULT_OS
        self.creation_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.id = req_id
