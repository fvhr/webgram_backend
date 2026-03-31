from fastapi import APIRouter

from src.presentation.api.v1.user.auth.router import auth_router
from src.presentation.api.v1.user.role.router import role_router
from src.presentation.api.v1.user.user.router import user_router

api_router = APIRouter(prefix='/api/v1', tags=['API v1'])

api_router.include_router(role_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)
