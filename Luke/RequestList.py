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

from Luke.Request import OS
from Luke.Request import OTHER_PROP
from Luke.Request import REQUIREMENTS
from Luke.utils import JsonUtils

CREATION_TIME = 'creation_time'
REQ_ID = 'id'


class RequestList(object):
    def __init__(self):
        pass

    @staticmethod
    def handle_new_request(request):
        json_req = dict()
        json_req[CREATION_TIME] = request.creation_time
        json_req[REQUIREMENTS] = request.requirements
        json_req[OTHER_PROP] = request.other_prop
        json_req[OS] = request.os
        json_req[REQ_ID] = request.id

        # add a request to a file with all open requests
        JsonUtils.append_json_to_file(json_req)
