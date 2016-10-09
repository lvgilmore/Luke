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

import json
import logging
import os
import uuid
from logging import getLogger

from flask import Flask
from flask import make_response
from flask import request

from Luke.Request import Request
from Luke.RequestList import RequestList
from Luke.matchMaker.MatchMaker import MatchMaker
from Luke.utils import JsonUtils

REQUIREMENTS = 'requirements'
OTHER_PROP = 'other_prop'

logger = getLogger(__name__)
logging.basicConfig(filename='LukeLogs.log',
                    format='[%(asctime)s] [%(levelname)s] %(module)s - %(funcName)s:   %(message)s',
                    level=logging.DEBUG,
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Api(object):
    def __init__(self):
        # set LUKE_PATH
        if 'LUKE_PATH' not in os.environ:
            os.environ['LUKE_PATH'] = os.path.join(os.path.dirname(__file__), "../../")
        # prepare pending requests file
        JsonUtils.init_file()

        # set up flask server
        self.web_server = Flask(__name__)
        self.init_routes()

    def init_routes(self):
        # self.web_server.error_handlers[None][404] = self.not_found
        self.web_server.add_url_rule(rule='/', endpoint='index', view_func=Api.index, methods=['GET'])
        self.web_server.add_url_rule(rule='/request', endpoint='requests', view_func=Api.handle_new_request,
                                     methods=['PUT', 'POST'])

    def handle_new_request(self, req, req_id=str(uuid.uuid4())):

        req = request.data

        logger.info("start handling new request id: " + req_id)
        json_req = json.loads(req)
        if self.check_if_req_valid(json_req):
            RequestList.handle_new_request(Request(json_req, req_id))

    @staticmethod
    def check_if_req_valid(req):
        if REQUIREMENTS not in req or OTHER_PROP not in req:
            logger.error("request is not in valid format")
            return False
        return True

    @staticmethod
    def handle_new_bare_metal(bare_metal):
        best_match_request = None
        match_maker = MatchMaker()

        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal.bare_metal)

        # read all requests from a file
        logger.debug("getting all request from file")
        req_list = JsonUtils.read_json_from_file()

        # find all requests that matches the requirements
        matched_requests_by_requirements = \
            match_maker.find_match_by_requirements(json_bare_metal, req_list)

        # check if list is not empty
        if matched_requests_by_requirements:
            # find match between bare metal and all requests
            best_match_request = match_maker.find_valid_candidate(
                json_bare_metal, matched_requests_by_requirements)

        if best_match_request:
            print(best_match_request.id)
            print(best_match_request.os)
            print("\nother prop:")
            for i in best_match_request.other_prop:
                print(i, best_match_request.other_prop[i])
            print("\nrequirements:")
            for i in best_match_request.requirements:
                print(i, best_match_request.requirements[i])
        else:
            print("no best match found")
            logger.info("no best match found")

        return best_match_request

    @staticmethod
    def not_found(*args):
        return make_response(json.dumps({'error': 'Not found'}), 404)

    @staticmethod
    def index():
        return json.dumps([{'index': 'main'}, {'supported methods': 'GET'}, {'apidoc': '/apidoc'}])

if __name__ == "__main__":
    pass
