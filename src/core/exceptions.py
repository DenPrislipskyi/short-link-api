from fastapi.responses import JSONResponse
from dataclasses import dataclass
from fastapi import FastAPI
from fastapi import Request


@dataclass(eq=False)
class InvalidUrlOrShortcode(Exception):
    status_code = 412

    @property
    def title(self) -> str:
        return "The provided shortcode or url is invalid"


@dataclass(eq=False)
class ShortcodeAlreadyExists(Exception):
    status_code = 409

    @property
    def title(self) -> str:
        return "Shortcode already in use"


@dataclass(eq=False)
class UrlNotProvided(Exception):
    status_code = 400

    @property
    def title(self) -> str:
        return "Url not present"


async def url_not_provided(request: Request, exc: UrlNotProvided) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.title},
    )


async def shortcode_already_exists(
    request: Request, exc: ShortcodeAlreadyExists
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.title},
    )


async def invalid_url_or_shortcode(
    request: Request, exc: InvalidUrlOrShortcode
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.title},
    )


def add_exceptions_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        UrlNotProvided,
        url_not_provided,
    )
    app.add_exception_handler(
        ShortcodeAlreadyExists,
        shortcode_already_exists,
    )
    app.add_exception_handler(
        InvalidUrlOrShortcode,
        invalid_url_or_shortcode,
    )
