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

from ConfigParser import ConfigParser
from logging import getLogger
from uuid import uuid4

from pymongo import MongoClient

from Luke.utils.JsonUtils import convert_from_json_to_obj

logger = getLogger(__name__)


class MList(object):
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read(os.path.join(os.environ['LUKE_PATH'], "resources/config.conf"))
        connection_uri = self.parser.get('mongodb', 'connection')
        db_name = self.parser.get('mongodb', 'dbname')
        self.database = MongoClient(connection_uri)[db_name]

    def _insert_to_collection(self, obj, collection):
        json_obj = convert_from_json_to_obj(obj)
        if 'id' in json_obj:
            json_obj['_id'] = json_obj.pop('id')
        logger.debug("appending id: " + json_obj['_id'] + " to collection" + collection)
        return self.database[collection].insert_one(json_obj).inserted_id

    def _update_collection(self, criteria, variable, obj, collection):
        return self.database[collection].update({'_id': criteria}, {"$set": {variable: obj}})

    def _load(self, collection, id):
        return self.database[collection].find_one({'_id': id})

    def _delete(self, collection):
        return self.database[collection].delete_many({})
