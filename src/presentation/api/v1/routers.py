from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.params import Depends

from src.application.common.use_cases.get_count_cdr_every_minute import GetCountCDREveryMinute
from src.presentation.api.v1.agent.router import agent_router, agent_operator_router
from src.presentation.api.v1.mappers import CommonPresentationMapper
from src.presentation.api.v1.numbers.router import numbers_router
from src.presentation.api.v1.queue.router import queue_router
from src.presentation.api.v1.schemas.responses import CdrEveryMinuteResponseSchema
from src.presentation.api.v1.user.auth.router import auth_router
from src.presentation.api.v1.user.role.router import role_router
from src.presentation.api.v1.user.user.router import user_admin_router, user_public_router
from src.presentation.api.v1.utils import require_roles

api_router = APIRouter(prefix='/backend/api/v1', tags=['API v1'])


@api_router.get('/cdr-count-every-minute', dependencies=[Depends(require_roles(['superadmin', 'supervisor']))],
                response_model=list[CdrEveryMinuteResponseSchema])
@inject
async def get_cdr_count_every_minute(year: int, month: int, day: int, use_case: FromDishka[GetCountCDREveryMinute]) -> \
        list[CdrEveryMinuteResponseSchema]:
    cdr_count_every_minute_dtos = await use_case(year, month, day)
    return [CommonPresentationMapper.to_cdr_count_every_minute_response(dto) for dto in cdr_count_every_minute_dtos]


api_router.include_router(role_router)
api_router.include_router(user_admin_router)
api_router.include_router(user_public_router)
api_router.include_router(auth_router)
api_router.include_router(agent_router)
api_router.include_router(queue_router)
api_router.include_router(agent_operator_router)
api_router.include_router(numbers_router)
