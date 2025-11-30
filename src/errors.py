from fastapi import status, Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI

class BookException(Exception):
    status_code: int = 400
    detail: str = "An error occurred"

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)

class InvalidToken(BookException):
    status_code = 401
    detail = "User has provided an invalid or expired token"

