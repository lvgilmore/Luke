from src.utils import JsonUtils

REQUIREMENTS = 'requirements'
OS = 'os'
OTHER = 'other'


class Request:

    def __init__(self, request_str):
        self.full_req = request_str
        self.requirements = None
        self.os = "Linux"
        self.other_prop = None

        self.parse_req(request_str)

    def parse_req(self, request_str):
        json_request = JsonUtils.convert_from_json_to_obj(request_str)
        for key in json_request.keys():
            if key == REQUIREMENTS:
                self.requirements = json_request[key]
            elif key == OS:
                self.os = json_request[key]
            else:
                self.other_prop = json_request[key]


    # def __init__(self, requirements={}, os="Linux", **kwargs):
    #     self.requirements = requirements
    #     self.os = os
    #     for key, value in kwargs:
    #         self.__dict__[key] = value
    #     pass

            # @staticmethod
    # def handle_new_request(request_str):
    #     # convert string request to json object
    #     json_request = JsonUtils.convert_from_json_to_obj(request_str)
    #
    #     # add a request to file of all open requests
    #     JsonUtils.write_json_to_file(json_request)
    #
    # @staticmethod
    # def update_request_score(request, score):
    #     JsonUtils.update_json_entry_with_score(request, score)
#
# if __name__ == "__main__":
#     req = Request()
#
#     entry = "{\"name\": \"name\", \"url\": \"url\"}"
#
#     req.handle_new_request(entry)
