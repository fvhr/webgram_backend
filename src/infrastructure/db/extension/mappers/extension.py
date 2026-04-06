from dataclasses import dataclass
from typing import final

from src.domain.extensions.entities.extension import Extension
from src.domain.extensions.value_objects.caller_id_number import CallerIdNumber
from src.domain.extensions.value_objects.extension_number import ExtensionNumber
from src.infrastructure.db.models.extension import ExtensionModel


@final
@dataclass(frozen=True, slots=True)
class ExtensionDBMapper:
    @staticmethod
    def to_entity(model: ExtensionModel) -> Extension:
        return Extension(
            extension_uuid=model.extension_uuid,
            extension_number=ExtensionNumber(model.extension_number),
            extension_password=model.extension_password,
            caller_id_name=model.caller_id_name,
            caller_id_number=CallerIdNumber(model.caller_id_number),
            domain_uuid=model.domain_uuid,
        )

    @staticmethod
    def to_model(entity: Extension) -> ExtensionModel:
        return ExtensionModel(
            extension_uuid=entity.extension_uuid,
            extension_number=entity.extension_number.value,
            extension_password=entity.extension_password,
            caller_id_name=entity.caller_id_name,
            caller_id_number=entity.caller_id_number.value,
            domain_uuid=entity.domain_uuid,
        )

    @staticmethod
    def update_model_from_entity(model: ExtensionModel, entity: Extension) -> None:
        model.extension_number = entity.extension_number.value
        model.extension_password = entity.extension_password
        model.caller_id_name = entity.caller_id_name
        model.caller_id_number = entity.caller_id_number.value
        model.domain_uuid = entity.domain_uuid
