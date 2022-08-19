from .base_error import BaseError
from enum import Enum

class QueryErrorType:
    TOKEN_INFO_EMPTY = 1
    UNKNOWN = 2

class QueryError(BaseError):
    def __init__(self, sg721, query, response, cause: Exception = None):
        super().__init__(response['message'], cause)
        self.sg712 = sg721
        self.query = query
        self.code = response['code']
        self.details = response['details']
        self.error_type = QueryErrorType.UNKNOWN

        if "TokenInfo<cosmwasm_std::results::empty::Empty>" in self.message:
            self.error_type = QueryErrorType.TOKEN_INFO_EMPTY
