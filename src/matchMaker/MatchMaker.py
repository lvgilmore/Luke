from utils.Utils import Utils

from src.Request import Request


class MatchMaker:
    def __init__(self):
        self.request_list = []

    def add_request_to_list(self, request):
        self.request_list.append(request)

if __name__ == "__main__":
    # jsonData = "{\"count\": 4," \
    #            "\"cpu\": 2," \
    #            "\"core\": 1}"
    jsonData = "[{\"count\" : \"2\", \"cpu\" : \"3\"}]"

    reqObj = Request(jsonData)
    Utils.write_json_to_file(jsonData)

    Utils.read_json_from_file()

    # req = Request("{\"count\": 5}")
    # m = MatchMaker()
    # m.request_list.append(req)
    # m.request_list.append(req)

    #
    # for req in m.request_list:
    #     print req['count']
