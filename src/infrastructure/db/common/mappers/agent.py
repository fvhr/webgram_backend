from dataclasses import dataclass
from typing import final

from sqlalchemy import Row

from src.application.agents.dtos.agent import AgentAtcDTO, AgentHistoryDTO


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

    @staticmethod
    def to_history_dto(model: Row) -> AgentHistoryDTO:
        return AgentHistoryDTO(
            start_stamp=model.start_stamp,
            duration=model.duration,
            direction=model.direction,
            caller_id_number=model.caller_id_number,
            destination_number=model.destination_number,
        )
