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
import os

from Luke.Api import Api

from Luke.BareMetal import BareMetal
from pymongo.database import Database
from unittest import TestCase
from uuid import uuid4

from Luke.MongoClient.MList import MList
from Luke.common.Status import Status


class TestMatchMaker(TestCase):
    def setUp(self):
        if 'LUKE_PATH' not in os.environ:
            os.environ['LUKE_PATH'] = os.path.join(os.path.dirname(__file__), "../../")
        self.mongo = MList()

    def tearDown(self):
        pass

    def test_connection(self):
        """make sure connection to db is established

        :return: no best match
        """
        self.assertIsInstance(self.mongo.database, Database)

    def test_insert_to_collection(self):
        uid = str(uuid4())
        _id = self.mongo._insert_to_collection({"id": uid}, "test")
        self.assertEqual(uid, _id)
        self.assertDictContainsSubset({"_id": uid}, self.mongo.database["test"].find_one({"_id": uid}))

    def test_update_collection(self):
        self.mongo._delete('test')
        uid = str(uuid4())
        old_value = 123
        self.mongo._insert_to_collection({"id": uid, "name": old_value}, "test")
        new_value = 123456
        self.mongo._update_collection(uid, "name", new_value, 'test')
        self.assertDictContainsSubset({"_id": uid}, self.mongo.database["test"].find_one({"name": new_value}))

    def test_load_collection(self):
        uid = str(uuid4())
        self.mongo._insert_to_collection({"id": uid, "name": 123}, "test")
        result = self.mongo._load("test", uid)
        self.assertEqual(123, result['name'])

    def test_bm(self):
        """
        one request with requirements that match bare metal, status changed to matched
        :return: request
        """
        req_id = str(uuid4())
        req = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
              "\"Vendor\": \"vend\"}," \
              "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
              "\"NICs\": {\"ens33\": " \
              "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
              \"Type\": \"Twisted Pair\"}}," \
              " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
              "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
              "\"Model\": \"mod\", \"profile\": \"common\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                     \"Type\": \"Twisted Pair\", \"ip\": \"192.168.0.4\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        self.api = Api()
        self.api.handle_new_request(req, req_id)
        bm = BareMetal(bare_metal)
        self.api.handle_new_bare_metal(bm)
        result = self.mongo._load("bare_metals", bm.id)
        self.assertEqual(result['status'], Status.matched)

    # def test_delete_collection(self):
    #     self.mongo._delete('requests')
    #     self.mongo._delete('bare_metals')
