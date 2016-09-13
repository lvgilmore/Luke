from src.matchMaker.MatchMaker import MatchMaker
from src.utils.JsonUtils import JsonUtils


class BareMetal:
    def __init__(self, bare_metal_str):
        self.handle_new_bare_metal(bare_metal_str)

    @staticmethod
    def handle_new_bare_metal(bare_metal_str):
        json_bare_metal = JsonUtils.convert_from_json_to_obj(bare_metal_str)

        request = MatchMaker().find_match(json_bare_metal)
        print request


if __name__ == "__main__":
    BareMetal("{\"name\": \"name1\", \"url\": \"url\"}")
