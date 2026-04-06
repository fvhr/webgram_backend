from dataclasses import dataclass
from typing import final

from sqlalchemy import Row

from src.application.agents.dtos.agent import AgentAtcDTO


@final
@dataclass(frozen=True, slots=True)
class AgentGatewayDBMapper:
    @staticmethod
    def to_entity(model: Row) -> AgentAtcDTO:
        return AgentAtcDTO(
            agent_uuid=model.call_center_agent_uuid,
            agent_name=model.agent_name,
            agent_number=model.agent_id,
            agent_password=model.agent_password,
            domain_uuid=model.domain_uuid,
        )
