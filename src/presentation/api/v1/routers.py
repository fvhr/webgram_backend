from fastapi import APIRouter

from src.presentation.api.v1.agent.router import agent_router
from src.presentation.api.v1.queue.router import queue_router
from src.presentation.api.v1.user.auth.router import auth_router
from src.presentation.api.v1.user.role.router import role_router
from src.presentation.api.v1.user.user.router import user_admin_router, user_public_router

api_router = APIRouter(prefix='/api/v1', tags=['API v1'])

api_router.include_router(role_router)
api_router.include_router(user_admin_router)
api_router.include_router(user_public_router)
api_router.include_router(auth_router)
api_router.include_router(agent_router)
api_router.include_router(queue_router)
