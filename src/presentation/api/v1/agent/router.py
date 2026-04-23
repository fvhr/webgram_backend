from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.application.agents.use_cases.end_call import EndCallUseCase
from src.application.agents.use_cases.get_free_agents import GetFreeAgentsUseCase
from src.application.agents.use_cases.set_queues import SetQueuesUseCase
from src.application.agents.use_cases.set_status import SetStatusUseCase
from src.application.agents.use_cases.set_user import SetUserUseCase
from src.application.agents.use_cases.spy_agent import SpyAgentUseCase
from src.application.user.use_cases.users.get_user import GetUserUseCase
from src.presentation.api.v1.agent.mappers import AgentPresentationMapper
from src.presentation.api.v1.agent.schemas.responses import AgentResponseSchema, AgentFreeResponseSchema
from src.presentation.api.v1.agent.schemas.schema import SetStatusAgent, SetQueuesAgent
from src.presentation.api.v1.user.mappers import UserPresentationMapper
from src.presentation.api.v1.user.schemas.responses import UserResponseSchema
from src.presentation.api.v1.utils import require_roles

agent_router = APIRouter(prefix='/agent', tags=['Agent'],
                         dependencies=[Depends(require_roles(['superadmin', 'supervisor']))])


@agent_router.get('/free-agents', response_model=list[AgentFreeResponseSchema])
@inject
async def get_free_agents(
        use_case: FromDishka[GetFreeAgentsUseCase]
) -> list[AgentFreeResponseSchema]:
    agents_dto = await use_case()
    return [AgentPresentationMapper.to_free_response(agent_dto) for agent_dto in agents_dto]


@agent_router.post('/set-user', response_model=UserResponseSchema)
@inject
async def set_user(agent_uuid: UUID, user_uuid: UUID, set_user_use_case: FromDishka[SetUserUseCase],
                   get_user_use_case: FromDishka[GetUserUseCase]) -> UserResponseSchema:
    await set_user_use_case(str(agent_uuid), user_uuid)
    user_dto = await get_user_use_case(str(user_uuid))
    return UserPresentationMapper.to_response(user_dto)


@agent_router.post('/set-status')
@inject
async def set_status(data: SetStatusAgent, use_case: FromDishka[SetStatusUseCase]) -> None:
    await use_case(str(data.agent_uuid), data.agent_status)


@agent_router.post('/end-call/{call_uuid}')
@inject
async def end_call(call_uuid: UUID, use_case: FromDishka[EndCallUseCase]) -> None:
    await use_case(str(call_uuid))


@agent_router.post('/spy-agent/{call_uuid}')
@inject
async def spy_agent(call_uuid: UUID, victim_agent_number: str, spy_agent_number: str, domain_uuid: UUID,
                   use_case: FromDishka[SpyAgentUseCase]) -> None:
    await use_case(str(call_uuid), victim_agent_number, spy_agent_number, str(domain_uuid))


@agent_router.post('/set-queues', response_model=AgentResponseSchema)
@inject
async def set_queues(data: SetQueuesAgent, use_case: FromDishka[SetQueuesUseCase]) -> AgentResponseSchema:
    agent_dto = await use_case(str(data.agent_uuid), [str(queue_uuid) for queue_uuid in data.queue_uuids])
    return AgentPresentationMapper.to_response(agent_dto)
