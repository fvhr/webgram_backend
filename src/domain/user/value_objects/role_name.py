from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.user.exceptions import ValidateError


@dataclass(frozen=True)
class RoleName(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not self.value:
            raise ValidateError('role name dont = 0')
        if len(self.value) > 32:
            raise ValidateError('role name too long')
