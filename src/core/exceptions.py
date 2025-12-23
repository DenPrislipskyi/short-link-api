from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class APIException(Exception):
    status_code = 500
    default_message = "Internal server error"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class InvalidUrlOrShortcode(APIException):
    status_code = 412
    default_message = "The provided shortcode/url is invalid"


class ShortcodeAlreadyExists(APIException):
    status_code = 409
    default_message = "Shortcode already in use"


class UrlNotProvided(APIException):
    status_code = 400
    default_message = "Url not present"


class UpdateIdDoesNotExist(APIException):
    status_code = 401
    default_message = "The provided update ID does not exist"


class ShortcodeNotFound(APIException):
    status_code = 404
    default_message = "Shortcode not found"


async def api_exception_handler(
    request: Request,
    exc: APIException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


def add_exceptions_handlers(app: FastAPI) -> None:
    app.add_exception_handler(APIException, api_exception_handler)
