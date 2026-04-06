from dataclasses import dataclass

from src.application.common.ports.atc_gateway import AtcGatewayProtocol
from src.application.extensions.ports.mapper import ExtensionDtoEntityMapperProtocol
from src.application.extensions.ports.repository import ExtensionRepositoryProtocol
from src.logger import logger


@dataclass
class SyncExtensionService:
    _extension_repository: ExtensionRepositoryProtocol
    _atc_gateway: AtcGatewayProtocol
    _extension_mapper: ExtensionDtoEntityMapperProtocol

    async def __call__(self) -> None:
        now_extensions = await self._extension_repository.get_extensions()
        update_extensions = await self._atc_gateway.get_atc_extensions()
        await self._extension_repository.create_or_update_all_extensions(
            [self._extension_mapper.to_entity(dto) for dto in update_extensions])
        delete_uuids_set = set([entity.extension_uuid for entity in now_extensions]) - set(
            [dto.extension_uuid for dto in update_extensions])

        for _uuid in delete_uuids_set:
            await self._extension_repository.delete_extension(str(_uuid))
        logger.info(f'Количество extension в системе: {len(update_extensions)}')
