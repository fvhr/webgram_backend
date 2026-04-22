from dataclasses import dataclass
from typing import final

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.queues.dtos.queue import ViewQueueDTO
from src.application.queues.ports.repository import ViewQueueRepositoryProtocol
from src.infrastructure.db.exceptions import RepositoryError
from src.infrastructure.db.models import QueueModel
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ViewQueueRepositorySQLAlchemy(ViewQueueRepositoryProtocol):
    session: AsyncSession
    mapper: QueueDBMapper

    async def get_queue(self, queue_uuid: str) -> ViewQueueDTO | None:
        try:
            stmt = select(QueueModel).where(
                QueueModel.queue_uuid == queue_uuid).options(
                selectinload(QueueModel.domain),
            )
            result = await self.session.execute(stmt)
            queue_model = result.scalar_one_or_none()
            if queue_model is None:
                return None
            return self.mapper.to_view_dto(queue_model)
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to retrieve queue by queue_uuid '{queue_uuid}': {e}")
            raise RepositoryError(
                f"Failed to retrieve queue by queue_uuid '{queue_uuid}': {e}"
            ) from e
