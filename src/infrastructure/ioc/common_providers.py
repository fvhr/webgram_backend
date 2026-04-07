from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.application.common.ports.external import AtcGatewayProtocol
from src.application.common.service.collect_handlers_service import CollectHandlersService
from src.application.domain.event_handlers.heartbeat import DomainHeartbeatEventHandler
from src.application.user.ports.auth import AuthentificationProtocol
from src.domain.services.password_hash_service import PasswordHashService
from src.infrastructure.auth.authentification_from_auth_x import AuthentificationAuthX
from src.infrastructure.db.common.atc_gateway import SqlAlchemyAtcGateway
from src.infrastructure.db.common.mappers.agent import AgentGatewayDBMapper
from src.infrastructure.db.common.mappers.domain import DomainGatewayDBMapper
from src.infrastructure.db.common.mappers.extension import ExtensionGatewayDBMapper
from src.infrastructure.db.common.mappers.queue import QueueGatewayDBMapper
from src.infrastructure.fs_events.fs_events import FreeSwitchEventListen
from src.settings import Settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class PasswordHashServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_hash_service(self) -> PasswordHashService:
        return PasswordHashService()


class AtcGatewayProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_atc_gateway_provider(self, session: AsyncSession, domain_mapper: DomainGatewayDBMapper,
                                 agent_mapper: AgentGatewayDBMapper,
                                 extension_mapper: ExtensionGatewayDBMapper,
                                 queue_mapper: QueueGatewayDBMapper,
                                 settings: Settings) -> AtcGatewayProtocol:
        return SqlAlchemyAtcGateway(session=session, settings=settings,
                                    domain_mapper=domain_mapper, agent_mapper=agent_mapper,
                                    extension_mapper=extension_mapper, queue_mapper=queue_mapper)


class AuthentificationProvider(Provider):
    @provide(scope=Scope.APP)
    def get_authentification(self, settings: Settings) -> AuthentificationProtocol:
        return AuthentificationAuthX(_settings=settings)


class FreeswitchEventsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_collect_handlers_service(self,
                                     domain_heartbeat_handler: DomainHeartbeatEventHandler) -> CollectHandlersService:
        return CollectHandlersService(_domain_heartbeat_handler=domain_heartbeat_handler)

    @provide(scope=Scope.APP)
    def freeswitch_events(self, settings: Settings,
                          collect_handlers_service: CollectHandlersService) -> FreeSwitchEventListen:
        return FreeSwitchEventListen(settings=settings, collect_handlers_service=collect_handlers_service)


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> AsyncEngine:
        connect_args = {}
        if 'postgresql' in settings.DATABASE_URL:
            connect_args = {
                'statement_cache_size': 0,
                'prepared_statement_cache_size': 0,
            }
        return create_async_engine(
            url=settings.DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            connect_args=connect_args,
        )

    @provide(scope=Scope.APP)
    def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session


def get_common_providers() -> list[Provider]:
    return [
        SettingsProvider(),
        DatabaseProvider(),
        PasswordHashServiceProvider(),
        AuthentificationProvider(),
        AtcGatewayProvider(),
        FreeswitchEventsProvider(),
    ]
