from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import register_exceptions
from src.api.routers import router as test_router
from src.core.config import get_settings
from src.core.lifespan import lifespan


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exceptions(app)
    app.include_router(test_router)

    return app


app = create_app()
