import enum


class ResponseCode(enum.Enum):
    """success response code"""
    SUCCESS = "SUCCESS"

    """Resource / API Endpoint not found"""
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"

    """response related to unknown errors"""
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

    """response related to bad request and business validation failures"""
    BAD_REQUEST = "BAD_REQUEST"
    INVALID_REQUEST_DATA = "INVALID_REQUEST_DATA"

    """response related to authentication and authorisation validation failures"""
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    AUTHORISATION_FAILED = "AUTHORISATION_FAILED"
    INVALID_AUTHENTICATION_CREDENTIALS = "INVALID_AUTHENTICATION_CREDENTIALS"
    EMAIL_VERIFICATION_FAILED = "EMAIL_VERIFICATION_FAILED"
    """Too Many Requests"""
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"


class BaseResponse:

    def __init__(self, status, status_code, message, data):
        self.status = status
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_json(self):
        return {
            "status": self.status,
            "status_code": str(self.status_code.value),
            "message": self.message,
            "data": self.data,
        }

    @staticmethod
    def get_response(status=0, status_code=ResponseCode.UNKNOWN_ERROR, message=None, data=None):
        return BaseResponse(status, status_code, message, data).to_json()
