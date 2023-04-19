import base64


class Response():
    def __init__(self, is_success: bool, message: str | None, data):
        self.is_success = is_success
        self.message = message
        self.data = data


def blob_to_base64(blob):
    return (base64.b64encode(blob)).decode("utf-8")
