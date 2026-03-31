from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import Response
from fastapi.requests import Request

from src.application.user.service.login_service import LoginService
from src.application.user.service.resfresh_service import RefreshService
from src.presentation.api.v1.user.mappers import AuthPresentationMapper
from src.presentation.api.v1.user.schemas.responses import TokensResponseSchema, AccessTokenResponseSchema
from src.presentation.api.v1.user.schemas.schema import LoginSchema
from src.presentation.api.v1.utils import require_authorization
from src.settings import Settings

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post('/login', response_model=TokensResponseSchema)
@inject
async def login(login_data: LoginSchema, response: Response, service: FromDishka[LoginService],
                settings: FromDishka[Settings]) -> TokensResponseSchema:
    login_dto = AuthPresentationMapper.to_login_dto(login_data)
    tokens_dto = await service(login_dto)
    response.set_cookie(
        key=settings.CONFIG.JWT_ACCESS_COOKIE_NAME,
        value=tokens_dto.access_token,
        httponly=True,
        max_age=int(settings.CONFIG.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
        samesite=settings.CONFIG.JWT_COOKIE_SAMESITE,
        secure=False,
    )
    response.set_cookie(
        key=settings.CONFIG.JWT_REFRESH_COOKIE_NAME,
        value=tokens_dto.refresh_token,
        httponly=True,
        max_age=int(settings.CONFIG.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
        samesite=settings.CONFIG.JWT_COOKIE_SAMESITE,
        secure=settings.CONFIG.JWT_COOKIE_SECURE,
    )
    return AuthPresentationMapper.to_tokens_response(tokens_dto)


@auth_router.post('/refresh',
                  response_model=AccessTokenResponseSchema, )
@inject
async def refresh_token(
        response: Response,
        request: Request,
        service: FromDishka[RefreshService],
        settings: FromDishka[Settings]
) -> AccessTokenResponseSchema:
    token = request.cookies.get(settings.CONFIG.JWT_REFRESH_COOKIE_NAME, None)
    access_token_dto = await service(token)
    response.set_cookie(
        key=settings.CONFIG.JWT_ACCESS_COOKIE_NAME,
        value=access_token_dto.access_token,
        httponly=True,
        max_age=int(settings.CONFIG.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
        samesite=settings.CONFIG.JWT_COOKIE_SAMESITE,
        secure=False,
    )
    return AuthPresentationMapper.to_access_token_response(access_token_dto)


@auth_router.post('/logout', dependencies=[Depends(require_authorization())])
@inject
async def logout(response: Response, settings: FromDishka[Settings]):
    response.delete_cookie(settings.CONFIG.JWT_ACCESS_COOKIE_NAME)
    response.delete_cookie(settings.CONFIG.JWT_REFRESH_COOKIE_NAME)
