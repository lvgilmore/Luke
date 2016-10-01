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
import logging

from Luke.matchMaker.MatchMaker import MatchMaker
from Luke.RequestList import RequestList
from Luke.utils import JsonUtils

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class Api(object):
    def __init__(self):
        JsonUtils.init_file()

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
            best_match_request = match_maker.find_valid_candidate(
                json_bare_metal, matched_requests_by_requirements)

        if best_match_request:
            logger.info("{}\n{}\n\nother prop:".format(best_match_request.id,
                                                       best_match_request.od))
            for i in best_match_request.other_prop:
                print(i, best_match_request.other_prop[i])
            logger.info("\nrequirements:")
            for i in best_match_request.requirements:
                print(i, best_match_request.requirements[i])
        else:
            logger.info("no best match found")

        return best_match_request


if __name__ == "__main__":
    pass
