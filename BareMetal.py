from utils.Utils import Utils


class BareMetal:
    def __init__(self, json_to_convert):
        barel_metal_object = self.convert_barel_metal_json(json_to_convert)
        print barel_metal_object['cpu']

    @staticmethod
    def convert_barel_metal_json(json_to_convert):
        return Utils.convert_from_json_to_obj(json_to_convert)


if __name__ == "__main__":
    req = BareMetal("{\"cpu\": 2}")
