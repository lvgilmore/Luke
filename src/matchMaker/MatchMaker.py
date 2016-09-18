class MatchMaker:

    def __init__(self):
        pass

    def find_match(self, bare_metal, req_list):
        """
        finds if there are equal keys and values in bare metal and in one of a requests
        if yes, updates the total curr_req_score of a specific request
        :param bare_metal:
        :param req_list:
        :return:
        """

        req_max_score = {'request': None, 'score': 0}

        """
        request[bare_metal_key] -> request["requirements"][bare_metal_key]
        for requi in request["requirements"]:
            make sure the requirement is met
        """
        for request in req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if bare_metal_key in request:
                    if bare_metal[bare_metal_key] == request[bare_metal_key]:
                        print("yes") # switch to logging
                        curr_req_score += MatchMaker.calc_score(bare_metal_key)

            # if total score of current request is bigger than the global value, update it
            if curr_req_score > req_max_score['score']:
                req_max_score = {'request': request, 'score': curr_req_score}

            # update the list with all requests
            # Request.update_request_score(request, curr_req_score)

        return req_max_score['request']

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
