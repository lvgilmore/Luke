import datetime
from logging import getLogger

# move to config file
REQUIREMENTS = 'requirements'
OS = 'os'
OTHER_PROP = 'other_prop'
DEFAULT_OS = 'Linux'

logger = getLogger(__name__)


class Request(object):
    def __init__(self, json_req, req_id):
        self.requirements = json_req[REQUIREMENTS] if REQUIREMENTS in json_req else {}
        self.other_prop = json_req[OTHER_PROP] if OTHER_PROP in json_req else {}
        self.os = json_req[OS] if OS in json_req else DEFAULT_OS
        self.creation_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.id = req_id
