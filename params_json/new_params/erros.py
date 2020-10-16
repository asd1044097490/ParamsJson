class Error(BaseException):
    def __init__(self, detail):
        self.detail = detail


class CheckError(Error):
    pass
