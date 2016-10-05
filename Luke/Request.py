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

# move to config file
REQUIREMENTS = 'requirements'
OS = 'os'
OTHER_PROP = 'other_prop'
DEFAULT_OS = 'Linux'

logger = getLogger(__name__)


class Request(object):
    def __init__(self, json_req, req_id):
        self.requirements = json_req[REQUIREMENTS] if REQUIREMENTS in json_req else {}
        self.other_prop = json_req[OTHER_PROP] if OTHER_PROP in json_req else {}
        self.os = json_req[OS] if OS in json_req else DEFAULT_OS
        self.creation_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.id = req_id
