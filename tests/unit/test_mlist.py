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

from pymongo.database import Database
from unittest import TestCase
from uuid import uuid4

from Luke.MongoClient.MList import MList


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
