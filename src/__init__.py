from fastapi import FastAPI

from src.core.exceptions import add_exceptions_handlers


def register_exceptions(
    app: FastAPI,
) -> None:
    add_exceptions_handlers(
        app,
    )
