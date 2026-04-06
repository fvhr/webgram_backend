from dataclasses import dataclass
from typing import final

from src.application.extensions.dtos.extension import ExtensionAtcDTO
from src.application.extensions.ports.mapper import ExtensionDtoEntityMapperProtocol
from src.domain.extensions.entities.extension import Extension
from src.domain.extensions.value_objects.caller_id_number import CallerIdNumber
from src.domain.extensions.value_objects.extension_number import ExtensionNumber


@final
@dataclass(frozen=True, slots=True)
class ExtensionDTOMapper(ExtensionDtoEntityMapperProtocol):

    def to_entity(self, dto: ExtensionAtcDTO) -> Extension:
        return Extension(
            extension_uuid=dto.extension_uuid,
            extension_number=ExtensionNumber(dto.extension_number),
            extension_password=dto.extension_password,
            caller_id_name=dto.caller_id_name,
            caller_id_number=CallerIdNumber(dto.caller_id_number),
            domain_uuid=dto.domain_uuid,
        )
