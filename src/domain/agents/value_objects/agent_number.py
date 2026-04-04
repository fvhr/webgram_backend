from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.exceptions import ValidateError


@dataclass(frozen=True)
class AgentNumber(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not self.value.isdigit():
            raise ValidateError('agent number must has digit only')