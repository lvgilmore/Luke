from Luke.utils import JsonUtils


class RequestList(object):

    def __init__(self):
        pass

    @staticmethod
    def handle_new_request(request):

        # convert string request to json object
        json_req = JsonUtils.convert_from_json_to_obj(request.full_req)

        # add creation time into a json
        json_req['creation_time'] = request.creation_time

        # add a request to a file with all open requests
        JsonUtils.append_json_to_file(json_req)
