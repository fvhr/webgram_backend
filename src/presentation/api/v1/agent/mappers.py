from dataclasses import dataclass
from typing import final

from src.application.agents.dtos.agent import AgentDTO, AgentFreeDTO, AgentHistoryDTO
from src.presentation.api.v1.agent.schemas.responses import AgentFreeResponseSchema, AgentResponseSchema, \
    AgentHistoryResponseSchema
from src.presentation.api.v1.queue.mappers import QueuePresentationMapper


@final
@dataclass(frozen=True, slots=True)
class AgentPresentationMapper:
    @staticmethod
    def to_free_response(dto: AgentFreeDTO) -> AgentFreeResponseSchema:
        """Convert Application DTO to API Response model."""
        return AgentFreeResponseSchema(
            agent_uuid=dto.agent_uuid,
            agent_name=dto.agent_name,
            agent_number=dto.agent_number,
        )

    @staticmethod
    def to_history_response(dto: AgentHistoryDTO) -> AgentHistoryResponseSchema:
        """Convert Application DTO to API Response model."""
        return AgentHistoryResponseSchema(
            start_stamp=dto.start_stamp,
            duration=dto.duration,
            direction=dto.direction,
            caller_id_number=dto.caller_id_number,
            destination_number=dto.destination_number,
        )

    @staticmethod
    def to_response(dto: AgentDTO) -> AgentResponseSchema:
        queues = [QueuePresentationMapper.to_response(queue_dto) for queue_dto in dto.queues]
        return AgentResponseSchema(
            agent_uuid=dto.agent_uuid,
            agent_name=dto.agent_name,
            agent_number=dto.agent_number,
            agent_password=dto.agent_password,
            domain_uuid=dto.domain_uuid,
            agent_status=dto.agent_status,
            queues=queues,
        )
