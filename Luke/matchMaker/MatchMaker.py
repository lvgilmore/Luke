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
import os

from ConfigParser import ConfigParser

from logging import getLogger

logger = getLogger(__name__)
DEFAULT_SECTION = 'SERVER'
SECTIONS_WITH_SUBSECTIONS = {'NICs', 'Disks'}


class MatchMaker(object):
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read(os.path.join(os.environ['LUKE_PATH'], "resources/scores.conf"))
        self.best_match_req = {'request': None, 'score': 0}

    def find_valid_candidate(self, bare_metal, req_list):

        """finds valid candidate

        finds if there are equal keys and values in bare metal and in
        one of the requests, if yes, updates the total curr_req_score
        of a specific request
        :param bare_metal:
        :param req_list:
        :return:
        """
        value = None

        for request in req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if request.requirements and \
                                bare_metal_key in request.requirements:
                    value = request.requirements[bare_metal_key]

                elif request.other_prop and \
                                bare_metal_key in request.other_prop:
                    value = request.other_prop[bare_metal_key]

                elif bare_metal_key in request.os and \
                                bare_metal[bare_metal_key] == request[bare_metal_key]:
                    value = request.os[bare_metal_key]

                curr_req_score = self.calc_score(value,
                                                 bare_metal[bare_metal_key],
                                                 bare_metal_key,
                                                 curr_req_score)

            # find the best match by the highest score
            self.compare_scores(curr_req_score, request)

        return self.best_match_req['request']

    def compare_scores(self, curr_req_score, request):
        if curr_req_score > self.best_match_req['score']:
            self.best_match_req = {'request': request, 'score': curr_req_score}
        elif self.best_match_req['score'] != 0 and \
                        self.best_match_req['score'] == curr_req_score:
            # compare by creation time
            if request.creation_time < \
                    self.best_match_req['request'].creation_time:
                self.best_match_req = {'request': request,
                                       'score': curr_req_score}
        return self.best_match_req['request']

    def calc_score(self, d1, d2, section, score=0):
        """
        comparing d1 to d2
        :param score:
        :param section:
        :param d1:
        :param d2:
        :return:
        """
        if isinstance(d1, dict) and isinstance(d2, dict):
            for key in d1.keys():
                if isinstance(d1[key], dict):
                    if section in SECTIONS_WITH_SUBSECTIONS:
                        score += self.calc_score(d1[key], d2[key], section, score)
                    else:
                        score += self.calc_score(d1[key], d2[key], key, score)
                else:
                    if d1[key] == d2[key]:
                        score += self.get_score_value(section, key)
        elif d1 == d2:
            score = self.get_score_value(DEFAULT_SECTION, section)

        return score

    def check_if_different(self, d1, d2):
        """
        comparing d1 to d2
        :param d1:
        :param d2:
        :param path:
        :return:
        """

        are_different = False

        if isinstance(d1, dict) and isinstance(d2, dict):
            for key in d1.keys():
                if key not in d2:
                    are_different = True
                    break
                else:
                    if isinstance(d1[key], dict):
                        are_different = self.check_if_different(d1[key], d2[key])
                        if are_different:
                            break
                    else:
                        if d1[key] != d2[key]:
                            are_different = True
                            break
        elif d1 != d2:
            are_different = True
        return are_different

    def find_match_by_requirements(self, bare_metal, req_list):
        """finds requests in which all requirements are met

        :param bare_metal:
        :param req_list:
        :return:
        """
        matched_req_by_requirements = []

        logger.debug("start finding requests that match requirements")
        for req in req_list:
            if not self.check_if_different(req.requirements, bare_metal):
                matched_req_by_requirements.append(req)

        logger.debug(
            "finding requests that match requirements ended with " +
            str(len(matched_req_by_requirements)) + " matching requests")
        return matched_req_by_requirements

    def get_score_value(self, section, key):
        """Get score of given key (option) in section from scores file

        :param section:
        :param key:
        :return:
        """
        score = 0

        if not self.parser.has_section(section.upper()):
            logger.debug("No section: " + section)
        elif not self.parser.has_option(section.upper(), key):
            logger.debug("No option: " + key + " in section: " + section)
        else:
            score = self.parser.get(section.upper(), key)

        return int(score)


if __name__ == "__main__":
    mm = MatchMaker()
