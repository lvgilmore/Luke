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

import json
import logging
import os
import uuid

from logging import getLogger

from Luke.BareMetal import BareMetal
from Luke.MongoClient.MBareMetalList import MBareMetalList
from Luke.MongoClient.MRequestList import MRequestList
from Luke.common.Status import Status
from Luke.utils.JsonUtils import convert_from_json_to_obj
from .CommitWorkflow import commit
from .matchMaker.MatchMaker import MatchMaker
from .Request import Request
from .utils import JsonUtils

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
        self.bare_metal_list = MBareMetalList()
        self.request_list = MRequestList()

    def handle_new_request(self, req, req_id=str(uuid.uuid4())):
        req = req.POST.get("request")
        logger.debug("start handling new request id: " + req_id + "request: " + req)
        json_req = JsonUtils.convert_from_json_to_obj(req)
        if self.check_if_req_valid(json_req):
            req = Request(json_req, req_id)
            self.request_list.handle_new_request(request=req)
            return req_id
        else:
            logger.error("request is not in valid format")
            return False

    @staticmethod
    def check_if_req_valid(req):
        return REQUIREMENTS in req and OTHER_PROP in req

    def handle_new_bare_metal(self, bare_metal):
        if isinstance(bare_metal, BareMetal):
            pass
        elif hasattr(bare_metal, 'META') and hasattr(bare_metal, 'POST'):
            logger.debug("treating bare_metal as HttpRequest")
            if 'ip' in convert_from_json_to_obj(bare_metal.POST.get("bare_metal")):
                ip = json.loads(bare_metal.POST.get("bare_metal"))['ip']
            else:
                ip = bare_metal.META["REMOTE_ADDR"]
            if bare_metal.META["REMOTE_HOST"] != ip:
                hostname = bare_metal.META["REMOTE_HOST"]
            else:
                hostname = None
            logger.debug("bare_metal_str " + str(bare_metal.POST))
            bare_metal = BareMetal(bare_metal_str=bare_metal.POST.get("bare_metal"),
                                   ip=ip, hostname=hostname)
        else:
            bare_metal = BareMetal(bare_metal)

        bm_id = self.bare_metal_list.handle_new_bare_metal(bare_metal=bare_metal)

        best_match_request = None
        match_maker = MatchMaker()

        json_bare_metal = JsonUtils.convert_from_json_to_obj(bare_metal)

        # read all requests from a file
        logger.debug("getting all request from file")
        req_list = self.request_list.load_requests()

        # find all requests that matches the requirements
        matched_requests_by_requirements = \
            match_maker.find_match_by_requirements(json_bare_metal, req_list)

        # check if list is not empty
        if matched_requests_by_requirements:
            # find match between bare metal and all requests
            best_match_request = match_maker.find_valid_candidate(
                json_bare_metal, matched_requests_by_requirements)

        if best_match_request:
            bm, r = commit(bare_metal=BareMetal(convert_from_json_to_obj(json_bare_metal)),
                           request=best_match_request)
            self.bare_metal_list.update_status(Status.matched, bm_id)
        else:
            logger.info("no best match found")

        return best_match_request, bare_metal
