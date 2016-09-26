import os
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

from configparser import ConfigParser

logger = getLogger(__name__)
DEFAULT_SECTION = 'SERVER'


class MatchMaker(object):

    def __init__(self):
        self.parser = ConfigParser()
        #        print(os.path.join(os.environ['LUKE_PATH'], "resources/scores.conf"))
        #         self.parser.read(os.path.join(os.environ['LUKE_PATH'], "resources/scores.conf"))

        # read scores from file
        self.parser.read(os.path.relpath('resources/scores.conf',
                                         os.path.join(os.path.dirname(__file__))))
        self.best_match_req = {'request': None, 'score': 0}

    def find_match_by_all_values(self, bare_metal, req_list):

        """finds valid candidates

        finds if there are equal keys and values in bare metal and in
        one of the requests, if yes, updates the total curr_req_score
        of a specific request
        :param bare_metal:
        :param req_list:
        :return:
        """

        for request in req_list:
            curr_req_score = 0
            for bare_metal_key in bare_metal.keys():
                if request.requirements and \
                                bare_metal_key in request.requirements:
                    curr_req_score += self.find_match(request.requirements[bare_metal_key],
                                                      bare_metal[bare_metal_key],
                                                      bare_metal_key)

                elif request.other_prop and \
                                bare_metal_key in request.other_prop:
                    curr_req_score += self.find_match(request.other_prop[bare_metal_key],
                                                      bare_metal[bare_metal_key],
                                                      bare_metal_key)

                elif bare_metal_key in request.os and \
                                bare_metal[bare_metal_key] == request[bare_metal_key]:
                    # curr_req_score += self.calc_score(bare_metal_key)
                    curr_req_score += self.find_match(request.os[bare_metal_key],
                                                      bare_metal[bare_metal_key],
                                                      bare_metal_key)

            # find the best match by the highest score
            self.compare_scores(curr_req_score, request)

        return self.best_match_req['request']

    def compare_scores(self, curr_req_score, request):
        if curr_req_score > self.best_match_req['score']:
            self.best_match_req = {'request': request, 'score': curr_req_score}
        elif self.best_match_req['score'] != 0 and self.best_match_req['score'] \
                == curr_req_score:
            # compare by creation time
            if request.creation_time > \
                    self.best_match_req['request'].creation_time:
                self.best_match_req = {'request': request,
                                       'score': curr_req_score}
        return self.best_match_req['request']

    def find_match(self, d1, d2, section, score=0):
        """
        comparing d1 to d2
        :param section:
        :param d1:
        :param d2:
        :param path:
        :return:
        """

        if isinstance(d1, dict) and isinstance(d2, dict):
            for key in d1.keys():
                if isinstance(d1[key], dict):
                    if section == 'NICs':
                        score += self.find_match(d1[key], d2[key], 'NICS', score)
                    elif section == 'Disks':
                        score += self.find_match(d1[key], d2[key], 'DISKS', score)
                    else:
                        score += self.find_match(d1[key], d2[key], key, score)
                else:
                    if d1[key] == d2[key]:
                        score += self.get_score(section, key)
        elif d1 == d2:
            score = self.get_score(DEFAULT_SECTION, section)
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
                if not d2.has_key(key):
                    are_different = True
                    break
                else:
                    if isinstance(d1[key], dict):
                        self.check_if_different(d1[key], d2[key])
                    else:
                        if d1[key] != d2[key]:
                            are_different = True
                            break
        elif d1 != d2:
            are_different = True
        return are_different

    def find_match_by_requirements(self, bare_metal, req_list):
        """
        finds requests in which all requirements are met
        :param bare_metal:
        :param req_list:
        :return:
        """
        matched_req_by_requirements = []

        for req in req_list:
            if not self.check_if_different(req.requirements, bare_metal):
                matched_req_by_requirements.append(req)

        return matched_req_by_requirements

    def get_score(self, section, key):
        """
        get score of given key (option) in section from scores file
        :param section:
        :param key:
        :return:
        """
        score = 0

        if not self.parser.has_section(section.upper()):
            print "no section: " + section
        elif not self.parser.has_option(section.upper(), key):
            print "no option: " + key + " in section: " + section
        else:
            score = self.parser.get(section.upper(), key)

        return int(score)


if __name__ == "__main__":
    mm = MatchMaker()
