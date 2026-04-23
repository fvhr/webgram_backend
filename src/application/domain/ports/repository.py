from abc import abstractmethod
from typing import Protocol

from src.domain.domain.entities.domain import Domain


class DomainRepositoryProtocol(Protocol):
    @abstractmethod
    async def create_or_update_domain(self, domain: Domain) -> Domain:
        raise NotImplementedError

    @abstractmethod
    async def delete_domain(self, domain_uuid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_domains(self) -> list[Domain]:
        raise NotImplementedError

    @abstractmethod
    async def get_domain_name_by_domain_uuid(self, domain_uuid: str) -> str | None:
        raise NotImplementedError

