import json

REQUESTS_FILE_NAME = "Requests.json"
SCORE_KEY = 'score'


class JsonUtils:

    @staticmethod
    def convert_from_json_to_obj(obj_to_convert):
        return json.loads(obj_to_convert)

    @staticmethod
    def write_json_to_file(json_entry):
        with open(REQUESTS_FILE_NAME, mode='r', encoding='utf-8') as f:
            feeds = json.load(f)
        with open(REQUESTS_FILE_NAME, mode='w', encoding='utf-8') as f:
            feeds.append(json_entry)
            json.dump(feeds, f)

    @staticmethod
    def init_file():
        # init file with an empty list
        with open(REQUESTS_FILE_NAME, mode='w', encoding='utf-8') as f:
            json.dump([], f)

    @staticmethod
    def read_json_from_file():
        with open(REQUESTS_FILE_NAME, mode='r') as f:
            requests_data = json.load(f)
            return requests_data

    @staticmethod
    def update_json_entry_with_score(request_to_update, score):
        """
        reads a content of a file, finds the given request and
        updates this entry with score value
        :param request_to_update:
        :param score:
        :return:
        """
        with open(REQUESTS_FILE_NAME, mode='r', encoding='utf-8') as f:
            requests = json.load(f)

            for request in requests:
                if request == request_to_update:
                    temp = request_to_update
                    temp[SCORE_KEY] = score
                    requests.pop(requests.index(request))
                    requests.append(temp)
                    break

        with open(REQUESTS_FILE_NAME, mode='w', encoding='utf-8') as f:
            json.dump(requests, f)
