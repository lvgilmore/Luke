from Luke.Request import REQUIREMENTS, OTHER_PROP, OS
from Luke.utils import JsonUtils

CREATION_TIME = 'creation_time'


class RequestList(object):

    def __init__(self):
        pass

    @staticmethod
    def handle_new_request(request):

        json_req = {}

        json_req[CREATION_TIME] = request.creation_time
        json_req[REQUIREMENTS] = request.requirements
        json_req[OTHER_PROP] = request.other_prop
        json_req[OS] = request.os

        # add a request to a file with all open requests
        JsonUtils.append_json_to_file(json_req)
