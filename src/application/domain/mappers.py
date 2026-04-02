from dataclasses import dataclass
from typing import final

from src.application.domain.dtos.domain import DomainDTO
from src.application.domain.ports.mappers import DomainDtoEntityMapperProtocol
from src.domain.domain.entities.domain import Domain
from src.domain.domain.value_objects.domain_name import DomainName


@final
@dataclass(frozen=True, slots=True)
class DomainDTOMapper(DomainDtoEntityMapperProtocol):

    def to_entity(self, dto: DomainDTO) -> Domain:
        return Domain(
            domain_uuid=dto.domain_uuid,
            domain_name=DomainName(value=dto.domain_name),
            domain_enabled=dto.domain_enabled,
            domain_description=dto.domain_description,
        )

    def to_dto(self, entity: Domain) -> DomainDTO:
        return DomainDTO(
            domain_uuid=entity.domain_uuid,
            domain_name=entity.domain_name.value,
            domain_enabled=entity.domain_enabled,
            domain_description=entity.domain_description,
        )
