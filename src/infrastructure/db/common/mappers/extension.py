from dataclasses import dataclass
from typing import final

from sqlalchemy import Row

from src.application.extensions.dtos.extension import ExtensionAtcDTO


@final
@dataclass(frozen=True, slots=True)
class ExtensionGatewayDBMapper:
    @staticmethod
    def to_entity(model: Row) -> ExtensionAtcDTO:
        return ExtensionAtcDTO(
            extension_uuid=model.extension_uuid,
            extension_number=model.extension,
            extension_password=model.password,
            caller_id_name=model.effective_caller_id_name,
            caller_id_number=model.effective_caller_id_number,
            domain_uuid=model.domain_uuid,
        )
