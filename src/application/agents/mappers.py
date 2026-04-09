from dataclasses import dataclass
from typing import final

from src.application.agents.dtos.agent import AgentAtcDTO
from src.application.agents.ports.mappers import AgentDtoEntityMapperProtocol
from src.domain.agents.entities.agent import Agent
from src.domain.agents.value_objects.agent_number import AgentNumber


@final
@dataclass(frozen=True, slots=True)
class AgentDTOMapper(AgentDtoEntityMapperProtocol):

    def to_dict(self, entity: Agent) -> dict:
        return {
            'agent_uuid': str(entity.agent_uuid),
            'agent_name': entity.agent_name,
            'agent_number': entity.agent_number.value,
            'agent_password': entity.agent_password,
            'domain_uuid': str(entity.domain_uuid),
            'user_uuid': str(entity.user_uuid) if entity.user_uuid else None,
            'agent_status': entity.agent_status,
        }

    def to_entity(self, dto: AgentAtcDTO) -> Agent:
        return Agent(
            agent_uuid=dto.agent_uuid,
            agent_name=dto.agent_name,
            agent_number=AgentNumber(dto.agent_number),
            agent_password=dto.agent_password,
            domain_uuid=dto.domain_uuid
        )
