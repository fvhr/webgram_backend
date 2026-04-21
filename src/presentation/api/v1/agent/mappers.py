from dataclasses import dataclass
from typing import final

from src.application.agents.dtos.agent import AgentDTO
from src.presentation.api.v1.agent.schemas.responses import AgentResponseSchema


@final
@dataclass(frozen=True, slots=True)
class AgentPresentationMapper:
    @staticmethod
    def to_response(dto: AgentDTO) -> AgentResponseSchema:
        """Convert Application DTO to API Response model."""
        return AgentResponseSchema(
            agent_uuid=dto.agent_uuid,
            agent_name=dto.agent_name,
            agent_number=dto.agent_number,
            agent_password=dto.agent_password,
            domain_uuid=dto.domain_uuid,
            agent_status=dto.agent_status,
        )
