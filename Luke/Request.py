import datetime
import json
import random

REQUIREMENTS = 'requirements'
OS = 'os'
OTHER_PROP = 'other_prop'
DEFAULT_OS = 'Linux'

class Request(object):

    def __init__(self, request_str):
        json_req = json.loads(request_str)

        self.requirements = json_req[REQUIREMENTS] if json_req.has_key(REQUIREMENTS) else {}
        self.other_prop = json_req[OTHER_PROP] if json_req.has_key(OTHER_PROP) else {}
        self.os = json_req[OS] if json_req.has_key(OS) else DEFAULT_OS
        self.creation_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
