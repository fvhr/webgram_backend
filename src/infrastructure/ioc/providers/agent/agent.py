from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.agents.event_handlers.channel_create import ChannelCreateEventHandler
from src.application.agents.event_handlers.status_change import AgentStatusChangeEventHandler
from src.application.agents.mappers import AgentDTOMapper
from src.application.agents.ports.mappers import AgentDtoEntityMapperProtocol
from src.application.agents.ports.repository import AgentRepositoryProtocol, ViewAgentRepositoryProtocol
from src.application.agents.service.sync_agent_service import SyncAgentService
from src.application.agents.use_cases.get_free_agents import GetFreeAgentsUseCase
from src.application.agents.use_cases.set_queues import SetQueuesUseCase
from src.application.agents.use_cases.set_status import SetStatusUseCase
from src.application.agents.use_cases.set_user import SetUserUseCase
from src.application.common.ports.external import AtcGatewayProtocol, WebSocketManagerProtocol, FreeswitchAPIProtocol
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol, FSAPIDtoEntityMapperProtocol
from src.application.common.service.get_calls_service import GetCallsService
from src.application.queues.ports.repository import ViewQueueRepositoryProtocol
from src.application.tiers.ports.repository import TierRepositoryProtocol, ViewTierRepositoryProtocol
from src.infrastructure.db.agent.mappers.agent import AgentDBMapper
from src.infrastructure.db.agent.repositories.agent import AgentRepositorySQLAlchemy
from src.infrastructure.db.agent.views.agent import ViewAgentRepositorySQLAlchemy
from src.infrastructure.db.common.mappers.agent import AgentGatewayDBMapper
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper


class AgentRepositoryProvider(Provider):
    @provide(scope=Scope.SESSION)
    async def get_agent_repository(self, session: AsyncSession, db_mapper: AgentDBMapper) \
            -> AgentRepositoryProtocol:
        return AgentRepositorySQLAlchemy(session=session, mapper=db_mapper)

    @provide(scope=Scope.SESSION)
    async def get_view_agent_repository(self, session: AsyncSession, db_mapper: AgentDBMapper) \
            -> ViewAgentRepositoryProtocol:
        return ViewAgentRepositorySQLAlchemy(session=session, mapper=db_mapper)


class AgentMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_agent_mapper(self) -> AgentDtoEntityMapperProtocol:
        return AgentDTOMapper()

    @provide(scope=Scope.SESSION)
    async def get_agent_db_mapper(self, queue_db_mapper: QueueDBMapper) -> AgentDBMapper:
        return AgentDBMapper(queue_db_mapper)

    @provide(scope=Scope.REQUEST)
    async def get_agent_gateway_db_mapper(self) -> AgentGatewayDBMapper:
        return AgentGatewayDBMapper()


class AgentServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def start_agent_service(
            self,
            agent_repository: AgentRepositoryProtocol,
            atc_gateway: AtcGatewayProtocol,
            agent_mapper: AgentDtoEntityMapperProtocol,
    ) -> SyncAgentService:
        return SyncAgentService(_agent_repository=agent_repository, _atc_gateway=atc_gateway,
                                _agent_mapper=agent_mapper)


class AgentEventHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def agent_status_change_event_handler(
            self,
            agent_repository: AgentRepositoryProtocol,
            event_mapper: EventDtoEntityMapperProtocol,
            ws_manager: WebSocketManagerProtocol,
            agent_mapper: AgentDtoEntityMapperProtocol,
    ) -> AgentStatusChangeEventHandler:
        return AgentStatusChangeEventHandler(_agent_repository=agent_repository, _event_mapper=event_mapper,
                                             _ws_manager=ws_manager, _agent_mapper=agent_mapper)

    @provide(scope=Scope.REQUEST)
    async def agent_channel_create_event_handler(
            self,
            get_calls_service: GetCallsService,
            ws_manager: WebSocketManagerProtocol,
    ) -> ChannelCreateEventHandler:
        return ChannelCreateEventHandler(_ws_manager=ws_manager, _get_calls_service=get_calls_service)


class AgentUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_free_agents_use_case(
            self,
            agent_repository: AgentRepositoryProtocol,
            agent_mapper: AgentDtoEntityMapperProtocol,
    ) -> GetFreeAgentsUseCase:
        return GetFreeAgentsUseCase(_agent_repository=agent_repository,
                                    _agent_mapper=agent_mapper)

    @provide(scope=Scope.REQUEST)
    async def set_user_use_case(
            self,
            agent_repository: AgentRepositoryProtocol,
    ) -> SetUserUseCase:
        return SetUserUseCase(_agent_repository=agent_repository)

    @provide(scope=Scope.REQUEST)
    async def set_status_use_case(
            self,
            fsapi: FreeswitchAPIProtocol,
    ) -> SetStatusUseCase:
        return SetStatusUseCase(_fsapi=fsapi)

    @provide(scope=Scope.REQUEST)
    async def set_queues_use_case(
            self,
            view_tier_repository: ViewTierRepositoryProtocol,
            tier_repository: TierRepositoryProtocol,
            queue_view_repository: ViewQueueRepositoryProtocol,
            agent_view_repository: ViewAgentRepositoryProtocol,
            fsapi: FreeswitchAPIProtocol,
    ) -> SetQueuesUseCase:
        return SetQueuesUseCase(_view_tier_repository=view_tier_repository,
                                _tier_repository=tier_repository,
                                _queue_view_repository=queue_view_repository,
                                _agent_view_repository=agent_view_repository,
                                _fsapi=fsapi,
                                )


def get_agent_providers() -> list[Provider]:
    return [
        AgentRepositoryProvider(),
        AgentMapperProvider(),
        AgentServiceProvider(),
        AgentEventHandlersProvider(),
        AgentUseCaseProvider(),
    ]
