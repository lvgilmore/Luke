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

from Luke.MongoClient.MList import MList
from Luke.Request import Request


class MRequestList(MList):
    def __init__(self):
        MList.__init__(self)

    def handle_new_request(self, request):
        return self._insert_to_collection(request, 'requests')

    def load_requests(self):
        json_reqs = self.database['requests'].find({})
        reqs = []
        for json_request in json_reqs:
            req_id = json_request.pop('_id')
            reqs.append(Request(json_req=json_request, req_id=req_id))
        return reqs
