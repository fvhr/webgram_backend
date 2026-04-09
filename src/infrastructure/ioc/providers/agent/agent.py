from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.agents.event_handlers.status_change import AgentStatusChangeEventHandler
from src.application.agents.mappers import AgentDTOMapper
from src.application.agents.ports.mappers import AgentDtoEntityMapperProtocol
from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.agents.service.sync_agent_service import SyncAgentService
from src.application.common.ports.external import AtcGatewayProtocol, WebSocketManagerProtocol
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol
from src.infrastructure.db.agent.mappers.agent import AgentDBMapper
from src.infrastructure.db.agent.repositories.agent import AgentRepositorySQLAlchemy
from src.infrastructure.db.common.mappers.agent import AgentGatewayDBMapper


class AgentRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_agent_repository(self, session: AsyncSession, db_mapper: AgentDBMapper) \
            -> AgentRepositoryProtocol:
        return AgentRepositorySQLAlchemy(session=session, mapper=db_mapper)


class AgentMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_agent_mapper(self) -> AgentDtoEntityMapperProtocol:
        return AgentDTOMapper()

    @provide(scope=Scope.REQUEST)
    async def get_agent_db_mapper(self) -> AgentDBMapper:
        return AgentDBMapper()

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


def get_agent_providers() -> list[Provider]:
    return [
        AgentRepositoryProvider(),
        AgentMapperProvider(),
        AgentServiceProvider(),
        AgentEventHandlersProvider(),
    ]
