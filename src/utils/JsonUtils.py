import io
import json

from src.Request import Request, OTHER_PROP, OS, REQUIREMENTS

REQUESTS_FILE_NAME = "Requests.json"
SCORE_KEY = 'score'


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
    req = Request(json.dumps(request))
    for key in request.keys():
        if key == REQUIREMENTS:
            req.requirements = request[key]
        elif key == OS:
            req.os = request[key]
        elif key == OTHER_PROP:
            req.other_prop = request[key]
    return req
