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

import io
import json
from logging import getLogger

from Request import Request
from common import constants

REQUESTS_FILE_NAME = "Requests.json"

logger = getLogger(__name__)


def convert_from_json_to_obj(obj_to_convert):
    return json.loads(obj_to_convert)


def append_json_to_file(json_entry):
    with io.open(REQUESTS_FILE_NAME, mode='r', encoding='utf-8') as f:
        feeds = json.load(f)
    with io.open(REQUESTS_FILE_NAME, mode='w', encoding='utf-8') as f:
        feeds.append(json_entry)
        f.write(unicode(json.dumps(feeds, ensure_ascii=False)))


def init_file():
    # init file with an empty list
    try:
        with io.open(REQUESTS_FILE_NAME, mode='r') as f:
            f.close()
    except IOError:
        logger.debug("start initialize file: " + REQUESTS_FILE_NAME)
        with io.open(REQUESTS_FILE_NAME, mode='w', encoding="utf-8") as f:
            f.write(unicode(json.dumps([], ensure_ascii=False)))
            f.close()
            logger.debug("initialize file: " + REQUESTS_FILE_NAME + " ended successfully")


def read_json_from_file():
    with io.open(REQUESTS_FILE_NAME, mode='r') as f:
        requests = json.load(f)
        return parse_requests_to_obj(requests)


def parse_requests_to_obj(requests):
    requests_list_obj = []

    for request in requests:
        requests_list_obj.append(parse_req(request))

    return requests_list_obj


def parse_req(request):
    req = Request(request, request['id'])
    for key in request.keys():
        if key == constants.REQS:
            req.requirements = request[key]
        elif key == constants.OS:
            req.os = request[key]
        elif key == constants.OTHER_PROP:
            req.other_prop = request[key]
    return req
