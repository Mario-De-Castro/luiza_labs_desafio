from fastapi import HTTPException

class SchemaValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)
        self._message = message


class GenericExceptions(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=500, detail=message)
        self._message = message

class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Unauthorized access. Please provide valid credentials."):
        super().__init__(status_code=401, detail=message)
        self._message = message

class DataAlreadyExistsException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=409, detail=message)
        self._message = message
