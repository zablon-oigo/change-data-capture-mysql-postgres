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

class UserAlreadyExists(BookException):
    status_code = 409
    detail = "User already exists with this email"

class AccountNotVerified(Exception):
    """Exception raised when the user account is not verified."""
    pass


class BookNotFound(BookException):
    status_code = 404
    detail = "Book not found"

class TagAlreadyExists(BookException):
    status_code = 409
    detail = "Tag already exists"

class TagNotFound(BookException):
    status_code = 404
    detail = "Tag not found"

class InvalidCredentials(BookException):
    status_code = 400
    detail = "Invalid email or password"

class UserNotFound(BookException):
    status_code = 404
    detail = "User not found"

class RevokedToken(BookException):
    status_code = 401
    detail = "Token has been revoked"

class AccessTokenRequired(BookException):
    status_code = 401
    detail = "Access token required"

class RefreshTokenRequired(BookException):
    status_code = 403
    detail = "Refresh token required"

class InsufficientPermission(BookException):
    status_code = 401
    detail = "Insufficient permission"


def create_exception_handler(status_code: int, initial_detail: dict):
    async def handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status_code,
            content=initial_detail
        )
    return handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not Verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details"
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid email or password",
                "error_code": "invalid_credentials",
            },
        ),
    )


