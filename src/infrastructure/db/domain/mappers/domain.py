from dataclasses import dataclass
from typing import final

from src.domain.domain.entities.domain import Domain
from src.domain.domain.value_objects.domain_name import DomainName
from src.infrastructure.db.models import DomainModel


@final
@dataclass(frozen=True, slots=True)
class DomainDBMapper:
    @staticmethod
    def to_entity(model: DomainModel) -> Domain:
        return Domain(
            domain_uuid=model.domain_uuid,
            domain_name=DomainName(model.domain_name),
            domain_enabled=model.domain_enabled,
            domain_description=model.domain_description,
        )

    @staticmethod
    def to_model(entity: Domain) -> DomainModel:
        return DomainModel(
            domain_uuid=entity.domain_uuid,
            domain_name=entity.domain_name.value,
            domain_enabled=entity.domain_enabled,
            domain_description=entity.domain_description,
        )

    @staticmethod
    def update_model_from_entity(model: DomainModel, entity: Domain) -> None:
        model.domain_name = entity.domain_name.value
        model.domain_enabled = entity.domain_enabled
        model.domain_description = entity.domain_description
