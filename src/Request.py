from src.utils.JsonUtils import JsonUtils


class Request:

    def __init__(self, requirements={}, os="Linux", **kwargs):
        self.requirements = requirements
        self.os = os
        for key, value in kwargs:
            self.__dict__[key] = value
        # SHOULD RUN ONLY ONCE
        JsonUtils.init_file()
        pass

    @staticmethod
    def handle_new_request(request_str):
        # convert string request to json object
        json_request = JsonUtils.convert_from_json_to_obj(request_str)

        # add a request to file of all open requests
        JsonUtils.write_json_to_file(json_request)

    @staticmethod
    def update_request_score(request, score):
        JsonUtils.update_json_entry_with_score(request, score)

if __name__ == "__main__":
    req = Request()

    entry = "{\"name\": \"name\", \"url\": \"url\"}"

    req.handle_new_request(entry)
