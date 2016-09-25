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
    api = Api()
    req = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                                    \"Speed\": \"2201.000\", \"Cores\": \"1\"},"\
                                "\"Vendor\": \"vend\"},"\
        "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, "\
        "\"NICs\": {\"ens33\": "\
                        "{\"Speed\": \"Speed: 1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                                \"Type\": \"Port: Twisted Pair\"}},"\
        " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, "\
                    "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, "\
        "\"Model\": \"mod\"}}"

    bare_metal = "{\"Vendor\": \"vend\","\
                    " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                    \"Speed\": \"2201.000\", \"Cores\": \"1\"},"\
                    " \"Ram\": {\"Size\": \"3062784\"}, "\
                    "\"NICs\": {\"ens33\": "\
                                    "{\"Speed\": \"Speed: 1000Mb/s\", \
                                    \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Port: Twisted Pair\"}},"\
                    " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, "\
                                "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, "\
                    "\"Model\": \"mod\"}"
    api.handle_new_request(Request(req))
    api.handle_new_bare_metal(BareMetal(bare_metal))
