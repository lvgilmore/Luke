from ConfigParser import SafeConfigParser, NoSectionError, ConfigParser, NoOptionError
from logging import getLogger

from src.utils.ConfFileUtil import ConfFileUtil

logger = getLogger(__name__)
SECTION = 'asection'


class MatchMaker:

    def __init__(self):
        # read scores from file
        self.parser = ConfFileUtil.read_from_conf_file('../resources/scores.conf')

    def find_match_by_all_values(self, bare_metal, req_list):

        """
        finds if there are equal keys and values in bare metal and in one of a requests
        if yes, updates the total curr_req_score of a specific request
        :param bare_metal:
        :param req_list:
        :return:
        """

        best_match_req = {'request': None, 'score': 0}

        for request in req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if request.requirements is not None and\
                                bare_metal_key in request.requirements and\
                                bare_metal[bare_metal_key] == request.requirements[bare_metal_key]:
                    curr_req_score += self.calc_score(bare_metal_key)

                elif request.other_prop is not None and\
                    bare_metal_key in request.other_prop and\
                    bare_metal[bare_metal_key] == request.other_prop[bare_metal_key]:
                        curr_req_score += self.calc_score(bare_metal_key)

                elif bare_metal_key in request.os and\
                                bare_metal[bare_metal_key] == request[bare_metal_key]:
                    curr_req_score += self.calc_score(bare_metal_key)

            # compare by score
            if curr_req_score > best_match_req['score']:
                best_match_req = {'request': request, 'score': curr_req_score}
            elif best_match_req['score'] != 0 and best_match_req['score'] == curr_req_score:
                # compare by creation time
                if request.creation_time > best_match_req['request'].creation_time:
                    best_match_req = {'request': request, 'score': curr_req_score}
        return best_match_req['request']

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
            if request.requirements is not None:
                for requirements_key in request.requirements:
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

    # TODO decide what we prefer: there is another option, to use sections, and declare a default section,
    #  so when the score is not declared, it will search it in defaule section and init score with 0
    def calc_score(self, key):
        score = 0

        try:
            score = int(self.parser.get(SECTION, key))
            score = int(self.parser.get(SECTION, key))
        except NoSectionError as nse:
            print "calc_score: " + "NoSectionError " + nse.message
        except NoOptionError as noe:
            print "calc_score: " + "NoOptionError" + noe.message
        except ValueError as ve:
            print "calc_score: " + "ValueError " + ve.message

        return score


if __name__ == "__main__":
    mm = MatchMaker()

