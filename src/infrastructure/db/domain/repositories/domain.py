from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.domain.ports.repository import DomainRepositoryProtocol
from src.domain.domain.entities.domain import Domain
from src.infrastructure.db.domain.mappers.domain import DomainDBMapper
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError
from src.infrastructure.db.models import DomainModel
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DomainRepositorySQLAlchemy(DomainRepositoryProtocol):
    session: AsyncSession
    mapper: DomainDBMapper

    async def create_or_update_domain(self, domain: Domain) -> Domain | None:
        try:
            stmt = select(DomainModel).where(
                DomainModel.domain_uuid
                == domain.domain_uuid
            )
            result = await self.session.execute(stmt)
            domain_model = result.scalar_one_or_none()
            if domain_model:
                self.mapper.update_model_from_entity(domain_model, domain)
            else:
                domain_model = self.mapper.to_model(domain)
                self.session.add(domain_model)
            await self.session.commit()
            return domain
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving or update domain '{domain.domain_uuid}': {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving or update domain'{domain.domain_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to save or update domain'{domain.domain_uuid}': {e}"
            )
            raise RepositoryError(
                f"Failed to save or update domain'{domain.domain_uuid}': {e}"
            ) from e

    async def delete_domain(self, domain_uuid: str) -> None:
        try:
            stmt = delete(DomainModel).where(
                DomainModel.domain_uuid == domain_uuid
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to delete domain '{domain_uuid}': {e}"
            )
            raise RepositoryError(
                f"Failed to delete domain '{domain_uuid}': {e}"
            ) from e

    async def get_domains(self) -> list[Domain]:
        try:
            stmt = select(DomainModel)
            result = await self.session.execute(stmt)
            domain_models = result.scalars().all()
            return [
                self.mapper.to_entity(domain_model)
                for domain_model in domain_models
            ]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve domains: {e}')
            raise RepositoryError(f'Failed to retrieve domains: {e}') from e
