from src.BareMetal import BareMetal
from src.Request import Request
from src.RequestList import RequestList
from src.matchMaker.MatchMaker import MatchMaker
from src.utils import JsonUtils


class Api:

    def __init__(self):
        # SHOULD RUN ONLY ONCE
        # JsonUtils.init_file()
        self.json_bare_metal = None

    def handle_new_request(self, req):
        RequestList.handle_new_request(req)

    def handle_new_bare_metal(self, bare_metal):
        self.json_bare_metal = JsonUtils.convert_from_json_to_obj(bare_metal.bare_metal)

        self.find_match()

    def find_match(self):

        # read all requests from a file
        req_list = JsonUtils.read_json_from_file()

        # find match between bare metal and all requests
        best_request = MatchMaker().find_match(self.json_bare_metal, req_list)

        print best_request

if __name__ == "__main__":

    api = Api()
    api.handle_new_request(Request("{\"requirements\": \"name1\", \"os\": \"url\"}"))
    api.handle_new_bare_metal(BareMetal("{\"requirements\": \"name1\", \"os\": \"url\"}"))
