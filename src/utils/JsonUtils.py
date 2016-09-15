import io
import json

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
        requests_data = json.load(f)
        return requests_data


# there is no need in this function, delete it later
def update_json_entry_with_score(request_to_update, score):
    """
    reads a content of a file, finds the given request and
    updates this entry with score value
    :param request_to_update:
    :param score:
    :return:
    """
    with io.open(REQUESTS_FILE_NAME, mode='r', encoding='utf-8') as f:
        requests = json.load(f)

        for request in requests:
            if request == request_to_update:
                temp = request_to_update
                temp[SCORE_KEY] = score
                requests.pop(requests.index(request))
                requests.append(temp)
                break

    with io.open(REQUESTS_FILE_NAME, mode='w', encoding='utf-8') as f:
        json.dump(requests, f)
