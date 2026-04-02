from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.exceptions import ValidateError


@dataclass(frozen=True)
class DomainName(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not self.value:
            raise ValidateError('domain name dont = 0')