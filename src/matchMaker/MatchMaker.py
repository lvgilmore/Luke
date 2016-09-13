from src.Request import Request
from src.utils.JsonUtils import JsonUtils


class MatchMaker:
    def __init__(self):
        self.req_list = []
        self.req_max_score = {'request': None, 'score': 0}
        pass

    def find_match(self, bare_metal):
        """
        finds if there are equal keys and values in bare metal and in one of a requests
        if yes, updates the total curr_req_score of a specific request
        :param bare_metal:
        :return:
        """
        # read all requests from a file
        self.req_list = JsonUtils.read_json_from_file()

        for request in self.req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if bare_metal_key in request:
                    if bare_metal[bare_metal_key] == request[bare_metal_key]:
                        print("yes")
                        curr_req_score += self.calc_score(bare_metal_key)

            # if total score of current request is bigger than the global value, update it
            if curr_req_score > self.req_max_score['score']:
                self.update_req_max_score(request, curr_req_score)

            # update the list with all requests
            # Request.update_request_score(request, curr_req_score)

        return self.req_max_score['request']

    def update_req_max_score(self, request, score):
        self.req_max_score['request'] = request
        self.req_max_score['score'] = score

    @staticmethod
    def calc_score(key):
        # TODO read scores from a config file

        if key == "name":
            score = 2
        elif key == "url":
            score = 4

        return score


if __name__ == "__main__":
    pass
