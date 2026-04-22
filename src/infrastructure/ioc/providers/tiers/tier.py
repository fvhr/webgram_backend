from dishka import provide, Scope, Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.tiers.ports.repository import TierRepositoryProtocol, ViewTierRepositoryProtocol
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper
from src.infrastructure.db.tier.mappers.tier import TierDBMapper
from src.infrastructure.db.tier.repositories.tier import TierRepositorySQLAlchemy
from src.infrastructure.db.tier.views.tier import ViewTierRepositorySQLAlchemy


class TierRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_tier_repository(self, session: AsyncSession, db_mapper: TierDBMapper) \
            -> TierRepositoryProtocol:
        return TierRepositorySQLAlchemy(session=session, mapper=db_mapper)

    @provide(scope=Scope.REQUEST)
    async def get_view_tier_repository(self, session: AsyncSession, db_mapper: TierDBMapper) \
            -> ViewTierRepositoryProtocol:
        return ViewTierRepositorySQLAlchemy(session=session, mapper=db_mapper)


class TierMapperProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_tier_db_mapper(self, queue_db_mapper: QueueDBMapper) -> TierDBMapper:
        return TierDBMapper(queue_db_mapper)


def get_tier_providers() -> list[Provider]:
    return [
        TierRepositoryProvider(),
        TierMapperProvider(),
    ]
