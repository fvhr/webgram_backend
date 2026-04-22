from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.application.queues.use_cases.get_queues import GetQueuesUseCase
from src.presentation.api.v1.queue.mappers import QueuePresentationMapper
from src.presentation.api.v1.queue.schemas.responses import QueueResponseSchema
from src.presentation.api.v1.utils import require_roles

queue_router = APIRouter(prefix='', tags=['Queue'],
                         dependencies=[Depends(require_roles(['superadmin', 'supervisor']))])


@queue_router.get('/queues', response_model=list[QueueResponseSchema])
@inject
async def get_queues(
        use_case: FromDishka[GetQueuesUseCase]
) -> list[QueueResponseSchema]:
    queues_dto = await use_case()
    return [QueuePresentationMapper.to_response(queue_dto) for queue_dto in queues_dto]
