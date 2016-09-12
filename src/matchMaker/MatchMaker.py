from src.Request import Request
from src.utils.JsonUtils import JsonUtils


class MatchMaker:
    def __init__(self):
        pass

    def find_match(self, bare_metal):
        """
        finds if there are equal keys and values in bare metal and in one of a requests
        if yes, updates the total score of a specific request
        :param bare_metal:
        :return:
        """
        # read all requests from a file
        requests = JsonUtils.read_json_from_file()

        for request in requests:
            score = 0
            for bare_metal_key in bare_metal.keys():
                if bare_metal_key in request:
                    if bare_metal[bare_metal_key] == request[bare_metal_key]:
                        print("yes")
                        score += self.calc_score(bare_metal_key)
                Request.update_request_score(request, score)

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
