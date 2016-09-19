from logging import getLogger

logger = getLogger(__name__)


class MatchMaker:

    def __init__(self):
        pass

    @staticmethod
    def find_match_by_all_values(bare_metal, req_list):

        """
        finds if there are equal keys and values in bare metal and in one of a requests
        if yes, updates the total curr_req_score of a specific request
        :param bare_metal:
        :param req_list:
        :return:
        """

        best_match_req_list = []
        max_score = 0

        for request in req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if request.requirements:
                    if bare_metal_key in request.requirements:
                        if bare_metal[bare_metal_key] == request.requirements[bare_metal_key]:
                            curr_req_score += MatchMaker.calc_score(bare_metal_key)

                elif request.other_prop:
                    if bare_metal_key in request.other_prop:
                        if bare_metal[bare_metal_key] == request.other_prop[bare_metal_key]:
                            curr_req_score += MatchMaker.calc_score(bare_metal_key)

                elif bare_metal_key in request.os:
                    if bare_metal[bare_metal_key] == request[bare_metal_key]:
                        curr_req_score += MatchMaker.calc_score(bare_metal_key)

            # if total score of current request is bigger than the global value, update it
            if curr_req_score > max_score:
                # if list not empty
                if best_match_req_list:
                    # delete the values of the list
                    del best_match_req_list[:]

                # add a high scored req to list
                best_match_req_list.append(request)
                max_score = curr_req_score
            elif max_score != 0 and curr_req_score == max_score:
                best_match_req_list.append(request)
                max_score = curr_req_score

        return best_match_req_list

    @staticmethod
    def find_match_by_requirements(bare_metal, req_list):
        """
        finds requests in which all requirements are met
        :param bare_metal:
        :param req_list:
        :return:
        """
        matched_req_by_requirements = []

        for request in req_list:
            request_match = True
            if request.requirements:
                for requirements_key in request.requirements:
                    # if request_match:
                    if requirements_key not in bare_metal.keys():
                        request_match = False
                        break
                    else:
                        if request.requirements[requirements_key] != bare_metal[requirements_key]:
                            request_match = False
                            break
            if request_match:
                matched_req_by_requirements.append(request)

        return matched_req_by_requirements

    @staticmethod
    def calc_score(key):
        score = 0

        # TODO read scores from a config file

        if key == "name":
            score = 2
        elif key == "url":
            score = 4

        return score


if __name__ == "__main__":
    pass
