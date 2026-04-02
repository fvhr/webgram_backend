from dataclasses import dataclass
from typing import final

from sqlalchemy import Row

from src.domain.domain.entities.domain import Domain
from src.domain.domain.value_objects.domain_name import DomainName


@final
@dataclass(frozen=True, slots=True)
class DomainGatewayDBMapper:
    @staticmethod
    def to_entity(model: Row) -> Domain:
        return Domain(
            domain_uuid=model.domain_uuid,
            domain_name=DomainName(model.domain_name),
            domain_enabled=model.domain_enabled,
            domain_description=model.domain_description,
        )
