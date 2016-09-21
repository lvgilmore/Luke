import datetime


class Request:

    def __init__(self, request_str):
        self.requirements = None
        self.other_prop = None
        self.os = "Linux"
        self.creation_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.full_req = request_str
