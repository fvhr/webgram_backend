from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from redis import asyncio as aioredis

from src.application.agents.event_handlers.channel_create import ChannelCreateEventHandler
from src.application.agents.event_handlers.status_change import AgentStatusChangeEventHandler
from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.mappers import EventDTOMapper, FSAPIDTOMapper
from src.application.common.ports.external import AtcGatewayProtocol, WebSocketManagerProtocol, FreeswitchAPIProtocol, \
    RedisClientProtocol
from src.application.common.ports.mapper import EventDtoEntityMapperProtocol, FSAPIDtoEntityMapperProtocol
from src.application.common.service.collect_handlers_service import CollectHandlersService
from src.application.common.service.get_calls_service import GetCallsService
from src.application.domain.event_handlers.heartbeat import DomainHeartbeatEventHandler
from src.application.extensions.event_handlers.heartbeat import ExtensionHeartbeatEventHandler
from src.application.queues.event_handlers.heartbeat import QueueHeartbeatEventHandler
from src.application.user.ports.auth import AuthentificationProtocol
from src.domain.services.password_hash_service import PasswordHashService
from src.infrastructure.auth.authentification_from_auth_x import AuthentificationAuthX
from src.infrastructure.db.common.atc_gateway import SqlAlchemyAtcGateway
from src.infrastructure.db.common.mappers.agent import AgentGatewayDBMapper
from src.infrastructure.db.common.mappers.domain import DomainGatewayDBMapper
from src.infrastructure.db.common.mappers.extension import ExtensionGatewayDBMapper
from src.infrastructure.db.common.mappers.queue import QueueGatewayDBMapper
from src.infrastructure.fs_events.fs_events import FreeSwitchEventListen
from src.infrastructure.fs_events.mappers import EventMapper
from src.infrastructure.fsapi.fsapi import ASyncFSAPI
from src.infrastructure.redis.aioredis import AioredisClient
from src.infrastructure.websocket.ws_manager import WebSocketManager
from src.presentation.api.v1.websocket.connection_manager import ConnectionManager
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
    @provide(scope=Scope.REQUEST)
    def get_collect_handlers_service(self,
                                     domain_heartbeat_handler: DomainHeartbeatEventHandler,
                                     extension_heartbeat_handler: ExtensionHeartbeatEventHandler,
                                     queue_heartbeat_handler: QueueHeartbeatEventHandler,
                                     agent_status_change_handler: AgentStatusChangeEventHandler,
                                     agent_channel_create_handler: ChannelCreateEventHandler
                                     ) -> CollectHandlersService:
        return CollectHandlersService(_domain_heartbeat_handler=domain_heartbeat_handler,
                                      _extension_heartbeat_handler=extension_heartbeat_handler,
                                      _queue_heartbeat_handler=queue_heartbeat_handler,
                                      _agent_status_change_handler=agent_status_change_handler,
                                      _agent_channel_create_handler=agent_channel_create_handler)

    @provide(scope=Scope.APP)
    def event_mapper(self) -> EventMapper:
        return EventMapper()

    @provide(scope=Scope.APP)
    def event_dto_mapper(self) -> EventDtoEntityMapperProtocol:
        return EventDTOMapper()

    @provide(scope=Scope.REQUEST)
    def freeswitch_events(self, settings: Settings,
                          collect_handlers_service: CollectHandlersService,
                          event_mapper: EventMapper,
                          ) -> FreeSwitchEventListen:
        return FreeSwitchEventListen(settings=settings, collect_handlers_service=collect_handlers_service,
                                     mapper=event_mapper)


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

    @provide(scope=Scope.SESSION)
    async def get_session(
            self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis_pool(self, settings: Settings) -> aioredis.Redis:
        return aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    @provide(scope=Scope.APP)
    def get_redis_client(self, pool: aioredis.Redis) -> RedisClientProtocol:
        return AioredisClient(_redis=pool)


class WebSocketProvider(Provider):
    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()

    @provide(scope=Scope.APP)
    def get_websocket_manager(self, connection_manager: ConnectionManager) -> WebSocketManagerProtocol:
        return WebSocketManager(_connection_manager=connection_manager)


class FSAPIProvider(Provider):
    @provide(scope=Scope.APP)
    def fsapi_mapper(self) -> FSAPIDtoEntityMapperProtocol:
        return FSAPIDTOMapper()

    @provide(scope=Scope.APP)
    def get_fsapi(self, settings: Settings, mapper: FSAPIDtoEntityMapperProtocol) -> FreeswitchAPIProtocol:
        return ASyncFSAPI(settings, mapper)

    @provide(scope=Scope.REQUEST)
    def get_get_calls_service(self,
                              fsapi: FreeswitchAPIProtocol,
                              agent_repository: AgentRepositoryProtocol,
                              fsapi_mapper: FSAPIDtoEntityMapperProtocol,
                              ) -> GetCallsService:
        return GetCallsService(_fsapi=fsapi,
                               _agent_repository=agent_repository,
                               _fsapi_mapper=fsapi_mapper)


def get_common_providers() -> list[Provider]:
    return [
        SettingsProvider(),
        DatabaseProvider(),
        RedisProvider(),
        PasswordHashServiceProvider(),
        AuthentificationProvider(),
        AtcGatewayProvider(),
        FreeswitchEventsProvider(),
        WebSocketProvider(),
        FSAPIProvider(),
    ]
