from enum import Enum


class ResultStatus(Enum):
    Failure = 0
    Success = 1


class ErrorCodes(Enum):
    Unexpected = 0


class ResultError:
    def __init__(self, code: ErrorCodes, description):
        self.code = code
        self.description = description


class SensorResultModel:
    def __init__(self, status: ResultStatus, errors: ResultError, data):
        self.status = status
        self.errors = errors
        self.data = data
