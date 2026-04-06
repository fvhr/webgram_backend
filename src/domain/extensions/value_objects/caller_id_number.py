from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.exceptions import ValidateError


@dataclass(frozen=True)
class CallerIdNumber(ValueObject[str]):
    value: str | None

    def _validate(self) -> None:
        if self.value and not self.value.isdigit():
            raise ValidateError('caller id number must has digit only')