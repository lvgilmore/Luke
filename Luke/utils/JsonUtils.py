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

from Luke.Request import Request

REQUESTS_FILE_NAME = "Requests.json"
SCORE_KEY = 'score'
REQUIREMENTS = 'requirements'
OS = 'os'
OTHER_PROP = 'other_prop'


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
    with io.open(REQUESTS_FILE_NAME, mode='w', encoding="utf-8") as f:
        f.write(unicode(json.dumps([], ensure_ascii=False)))


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
    req = Request(request)
    for key in request.keys():
        if key == REQUIREMENTS:
            req.requirements = request[key]
        elif key == OS:
            req.os = request[key]
        elif key == OTHER_PROP:
            req.other_prop = request[key]
    return req


# there is no need in this function, delete it later
# def update_json_entry_with_score(request_to_update, score):
#     """
#     reads a content of a file, finds the given request and
#     updates this entry with score value
#     :param request_to_update:
#     :param score:
#     :return:
#     """
#     with io.open(REQUESTS_FILE_NAME, mode='r', encoding='utf-8') as f:
#         requests = json.load(f)
#
#         for request in requests:
#             if request == request_to_update:
#                 temp = request_to_update
#                 temp[SCORE_KEY] = score
#                 requests.pop(requests.index(request))
#                 requests.append(temp)
#                 break
#
#     with io.open(REQUESTS_FILE_NAME, mode='w', encoding='utf-8') as f:
#         json.dump(requests, f)
