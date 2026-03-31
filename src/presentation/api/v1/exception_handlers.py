from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.application.common.exceptions import AlreadyExistsError, NotFoundError
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RepositoryError)
    async def repository_error_api_exception_handler(
            request: Request,
            exc: RepositoryError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': str(exc)},
        )

    @app.exception_handler(ConflictRepositoryError)
    async def repository_conflict_error_api_exception_handler(
            request: Request,
            exc: ConflictRepositoryError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_api_exception_handler(
            request: Request,
            exc: NotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': str(exc)},
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_error_api_exception_handler(
            request: Request,
            exc: AlreadyExistsError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': str(exc)},
        )
