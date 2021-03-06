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


class MBareMetalList(MList):
    def __init__(self):
        MList.__init__(self)

    def handle_new_bare_metal(self, bare_metal):
        return self._insert_to_collection(bare_metal, 'bare_metals')

    def load_bare_metal(self, bm_id):
        return self._load('bare_metals', bm_id)

    def update_status(self, new_status, bm_id):
        return self._update_collection(criteria=bm_id, variable='status', obj=new_status, collection='bare_metals')

    def load_status(self, bm_id):
        res = self._load('bare_metals', bm_id)
        return res['status']
