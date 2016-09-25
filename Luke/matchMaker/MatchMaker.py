#! /usr/bin/python2.7

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from logging import getLogger
from Luke.utils.ConfFileUtil import ConfFileUtil

logger = getLogger(__name__)
SCORES_FILE = '../resources/scores.conf'
#SCORES_FILE = 'C:\\Users\\Yulia_tev\\PycharmProjects\\Luke\\resources\\scores.conf'


class MatchMaker(object):
    def __init__(self):
        # read scores from file
        # fn = os.path.dirname(os.path.abspath(__file__))
        # scores_file_path = os.path.relpath('resources/scores.conf', os.path.join(os.path.dirname(__file__)))
        # sdf = (os.path.join(os.path.abspath(os.path.dirname(__file__)), '..\\resources', 'scores.conf'))
        self.parser = ConfFileUtil.read_from_conf_file(SCORES_FILE)

    def find_match_by_all_values(self, bare_metal, req_list):

        """finds valid candidates

        finds if there are equal keys and values in bare metal and in
        one of the requests, if yes, updates the total curr_req_score
        of a specific request
        :param bare_metal:
        :param req_list:
        :return:
        """

        best_match_req = {'request': None, 'score': 0}

        for request in req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if request.requirements and \
                                bare_metal_key in request.requirements:
                    if self.find_diff(request.requirements[bare_metal_key], bare_metal[bare_metal_key]):
                        curr_req_score += self.calc_score(bare_metal_key)

                elif request.other_prop and \
                                bare_metal_key in request.other_prop:
                    if self.find_diff(request.other_prop[bare_metal_key], bare_metal[bare_metal_key]):
                        curr_req_score += self.calc_score(bare_metal_key)

                elif bare_metal_key in request.os and \
                                bare_metal[bare_metal_key] == request[bare_metal_key]:
                    curr_req_score += self.calc_score(bare_metal_key)

            # compare by score
            if curr_req_score > best_match_req['score']:
                best_match_req = {'request': request, 'score': curr_req_score}
            elif best_match_req['score'] != 0 and best_match_req['score'] \
                    == curr_req_score:
                # compare by creation time
                if request.creation_time > \
                        best_match_req['request'].creation_time:
                    best_match_req = {'request': request,
                                      'score': curr_req_score}
        return best_match_req['request']

    def find_diff(self, d1, d2, path=""):
        """
        comparing d1 to d2
        :param d1:
        :param d2:
        :param path:
        :return:
        """

        is_matches = True

        if isinstance(d1, dict) and isinstance(d2, dict):
            for key in d1.keys():
                if not d2.has_key(key):
                    is_matches = False
                    break
                else:
                    if isinstance(d1[key], dict):
                        self.find_diff(d1[key], d2[key], path)
                    else:
                        if d1[key] != d2[key]:
                            is_matches = False
                            break
        elif d1 != d2:
            is_matches = False
        return is_matches

    def find_match_by_requirements(self, bare_metal, req_list):
        """
        finds requests in which all requirements are met
        :param bare_metal:
        :param req_list:
        :return:
        """
        matched_req_by_requirements = []

        for req in req_list:
            if self.find_diff(req.requirements, bare_metal):
                matched_req_by_requirements.append(req)

        return matched_req_by_requirements

    def calc_score(self, key):
        score = 0
        try:
            score = int(self.parser.get_option(key))
        except ValueError as ve:
            print ("calc_score: " + "ValueError " + ve.message)

        return score


if __name__ == "__main__":
    mm = MatchMaker()
