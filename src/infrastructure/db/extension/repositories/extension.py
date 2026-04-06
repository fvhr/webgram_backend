from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.extensions.ports.repository import ExtensionRepositoryProtocol
from src.domain.extensions.entities.extension import Extension
from src.infrastructure.db.extension.mappers.extension import ExtensionDBMapper
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError
from src.infrastructure.db.models.extension import ExtensionModel
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExtensionRepositorySQLAlchemy(ExtensionRepositoryProtocol):
    session: AsyncSession
    mapper: ExtensionDBMapper

    async def create_or_update_all_extensions(self, extensions: list[Extension]) -> list[Extension]:
        try:
            for extension in extensions:
                stmt = select(ExtensionModel).where(
                    ExtensionModel.extension_uuid
                    == extension.extension_uuid
                )
                result = await self.session.execute(stmt)
                extension_model = result.scalar_one_or_none()
                if extension_model:
                    self.mapper.update_model_from_entity(extension_model, extension)
                else:
                    extension_model = self.mapper.to_model(extension)
                    self.session.add(extension_model)
            await self.session.commit()
            return extensions
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving or update extensions: {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving or update extensions: {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to save or update extensions: {e}"
            )
            raise RepositoryError(
                f"Failed to save or update extensions: {e}"
            ) from e

    async def delete_extension(self, extension_uuid: str) -> None:
        try:
            stmt = delete(ExtensionModel).where(
                ExtensionModel.extension_uuid == extension_uuid
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to delete extension '{extension_uuid}': {e}"
            )
            raise RepositoryError(
                f"Failed to delete extension '{extension_uuid}': {e}"
            ) from e

    async def get_extensions(self) -> list[Extension]:
        try:
            stmt = select(ExtensionModel)
            result = await self.session.execute(stmt)
            extension_models = result.scalars().all()
            return [
                self.mapper.to_entity(extension_model)
                for extension_model in extension_models
            ]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve extensions: {e}')
            raise RepositoryError(f'Failed to retrieve extensions: {e}') from e
