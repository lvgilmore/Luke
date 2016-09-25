import datetime
import json
import uuid

REQUIREMENTS = 'requirements'
OS = 'os'
OTHER_PROP = 'other_prop'
DEFAULT_OS = 'Linux'


class Request(object):
    def __init__(self, request_str, req_id = str(uuid.uuid4())):
        json_req = json.loads(request_str)

        self.requirements = \
            json_req[REQUIREMENTS] if REQUIREMENTS in json_req else {}
        self.other_prop = \
            json_req[OTHER_PROP] if OTHER_PROP in json_req else {}
        self.os = json_req[OS] if OS in json_req else DEFAULT_OS
        self.creation_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.id = req_id
