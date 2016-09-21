from Luke.BareMetal import BareMetal
from Luke.matchMaker.MatchMaker import MatchMaker
from Luke.Request import Request
from Luke.RequestList import RequestList
from Luke.utils import JsonUtils


class Api(object):

    def __init__(self):
        # SHOULD RUN ONLY ONCE
        JsonUtils.init_file()
        pass

    @staticmethod
    def handle_new_request(req):
        RequestList.handle_new_request(req)

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
            best_match_request = match_maker.find_match_by_all_values(
                json_bare_metal, matched_requests_by_requirements)

        if best_match_request:
            print (best_match_request.os)
            print ("\nother prop:")
            for i in best_match_request.other_prop:
                print (i, best_match_request.other_prop[i])
            print ("\nrequirements:")
            for i in best_match_request.requirements:
                print (i, best_match_request.requirements[i])
        else:
            print("no best match found")

if __name__ == "__main__":

    api = Api()
    api.handle_new_request(Request("{\"other_prop\": {\"name\": \"name1\"}}"))
    api.handle_new_request(Request("{\"requirements\": {\"cpu\": \"cpu\","
                                   " \"name1\": \"name1\",  \"id1\": \"id1\"},"
                                   " \"os\": \"Windows\"}"))
    api.handle_new_request(Request("{\"requirements\": {\"name\": \"name1\","
                                   " \"id\": \"id1\"}, \"os\": \"Linux\"}"))
    api.handle_new_request(Request("{\"requirements\": {\"name\": \"name1\","
                                   " \"id\": \"id1\"}, \"os\": \"Linux\"}"))
    api.handle_new_request(Request("{\"requirements\": {\"name\": \"name\","
                                   " \"url\": \"url\", \"id\": \"id1\"},"
                                   " \"os\": \"Linux\"}"))
    api.handle_new_bare_metal(BareMetal("{\"name\": \"name1\","
                                        " \"id\": \"id1\","
                                        " \"os\": \"os\"}"))
