import os
from dataclasses import dataclass

from src.application.common.ports.external import AtcGatewayProtocol


@dataclass
class GetCDRRecordUseCase:
    _atc_gateway: AtcGatewayProtocol

    async def __call__(self, call_uuid: str) -> str:
        file_path = await self._atc_gateway.get_record_path(call_uuid)
        if file_path is None or not (os.path.exists(file_path) and os.path.getsize(file_path) > 0):
            raise FileNotFoundError(f'File {call_uuid} not found.')
        return file_path
