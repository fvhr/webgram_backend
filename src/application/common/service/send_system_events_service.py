from dataclasses import dataclass

from src.application.common.ports.external import GetSystemResourcesProtocol, WebSocketManagerProtocol
from src.application.common.ports.mapper import SystemEventsDtoDictMapperProtocol
from src.domain.enums import WebsocketMessageTypes, WebsocketRoles


@dataclass
class SendSystemEventsService:
    _system_resources: GetSystemResourcesProtocol
    _mapper: SystemEventsDtoDictMapperProtocol
    _ws_manager: WebSocketManagerProtocol

    async def __call__(self) -> None:
        ram_dto = await self._system_resources.get_ram()
        cpu_dto = await self._system_resources.get_cpu()
        disk_dto = await self._system_resources.get_disk()
        data = self._mapper.to_dict(ram_dto, cpu_dto, disk_dto)
        await self._ws_manager.broadcast_message_to_role(WebsocketMessageTypes.SYSTEM_RESOURCES_MONITORING, data,
                                                 WebsocketRoles.DASHBOARD)
