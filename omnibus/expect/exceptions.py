class ExpectException(Exception):
    pass


class EofException(ExpectException):
    pass


class TimeoutException(ExpectException):
    pass
