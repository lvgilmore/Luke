import json
import uuid
from logging import getLogger

from Luke.Request import Request
from Luke.RequestList import RequestList
from Luke.matchMaker.MatchMaker import MatchMaker
from Luke.utils import JsonUtils

REQUIREMENTS = 'requirements'
OTHER_PROP = 'other_prop'

logger = getLogger(__name__)


class Api(object):
    def __init__(self):
        # if os.environ['LUKE_PATH'] == "":
        #     os.environ['LUKE_PATH'] = os.path.dirname(__file__)

        # SHOULD RUN ONLY ONCE
        JsonUtils.init_file()
        pass

    def handle_new_request(self, req, req_id=str(uuid.uuid4())):
        json_req = json.loads(req)
        if self.check_if_req_valid(json_req):
            RequestList.handle_new_request(Request(json_req, req_id))

    @staticmethod
    def check_if_req_valid(req):
        if REQUIREMENTS not in req or OTHER_PROP not in req:
            logger.error("request is not in valid format")
            print("request is not in valid format")
            return False
        return True

    @staticmethod
    def handle_new_bare_metal(bare_metal):
        best_match_request = None
        match_maker = MatchMaker()

        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal.bare_metal)

        # read all requests from a file
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

        return best_match_request


if __name__ == "__main__":
    pass
