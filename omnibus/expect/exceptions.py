class ExpectException(Exception):
    pass


class EofExpectException(ExpectException):
    pass


class TimeoutExpectException(ExpectException):
    pass
