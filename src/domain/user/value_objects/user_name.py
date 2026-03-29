from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.user.exceptions import ValidateError


@dataclass(frozen=True)
class UserName(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not self.value:
            raise ValidateError('user name dont = 0')
        if ' ' in self.value:
            raise ValidateError("' ' not supported in user name")
