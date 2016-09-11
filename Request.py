from utils.Utils import Utils


class Request:

    def __init__(self, json_to_convert):
        request_object = self.convert_request_json(json_to_convert)
        # print request_object['count']

    @staticmethod
    def convert_request_json(json_to_convert):
        return Utils.convert_from_json_to_obj(json_to_convert)

if __name__ == "__main__":
    req = Request("{\"count\": 4}")