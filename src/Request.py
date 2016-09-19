import datetime


class Request:

    def __init__(self, request_str):
        self.requirements = None
        self.other_prop = None
        self.os = "Linux"
        # self.creation_time = datetime.datetime.now()
        # self.full_req = request_str + self.creation_time.strftime("%I:%M%p on %B %d, %Y")
        self.full_req = request_str
