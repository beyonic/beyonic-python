class BeyonicError(Exception):
    pass
    """
    def __init__(self, message=None, http_body=None, http_status=None, json_body=None):
        super(BeyonicError, self).__init__(message)

        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
    """


class ResponseError(Exception):
    """
    Raised when the Beyonic API responds with an HTTP error
    """
    pass
