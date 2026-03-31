import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.ioc.di import get_providers
from src.logger import logger
from src.presentation.api.v1.exception_handlers import setup_exception_handlers
from src.presentation.api.v1.routers import api_router
from src.utils import start_default_functions


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info('Starting application...')
    asyncio.create_task(start_default_functions(_app))
    yield
    logger.info('Shutting down application...')


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title='Webgram Backend',
        version='1',
        description='Webgram Backend',
        lifespan=lifespan,
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            '*'
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    container: AsyncContainer = make_async_container(*get_providers())
    setup_dishka(container, app)

    setup_exception_handlers(app)
    app.include_router(api_router)

    return app


app = create_app()
