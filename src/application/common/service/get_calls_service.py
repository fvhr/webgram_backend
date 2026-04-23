from dataclasses import dataclass

from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.application.common.ports.external import FreeswitchAPIProtocol
from src.application.common.ports.mapper import FSAPIDtoEntityMapperProtocol
from src.logger import logger


@dataclass
class GetCallsService:
    _fsapi: FreeswitchAPIProtocol
    _agent_repository: AgentRepositoryProtocol
    _fsapi_mapper: FSAPIDtoEntityMapperProtocol

    async def get_calls(self) -> dict:
        calls_dto = await self._fsapi.get_calls_json()
        response = dict()
        for call_dto in calls_dto:
            try:
                if 'sofia/internal/' in call_dto.name:
                    call_dto.direction = 'outbound'
                    agent_uuid = await self._agent_repository.get_agent_uuid_by_agent_num(call_dto.cid_num)
                else:
                    call_dto.direction = 'inbound'
                    agent_uuid = await self._agent_repository.get_agent_uuid_by_agent_num(call_dto.b_cid_num)
                if agent_uuid:
                    if str(agent_uuid) not in response:
                        response[str(agent_uuid)] = []
                    response[str(agent_uuid)].append(self._fsapi_mapper.to_calls_dict(call_dto))
            except Exception as ex:
                logger.critical(str(ex))
        return response
