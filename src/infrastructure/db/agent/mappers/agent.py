from dataclasses import dataclass
from typing import final

from src.application.agents.dtos.agent import AgentDTO
from src.domain.agents.entities.agent import Agent
from src.domain.agents.value_objects.agent_number import AgentNumber
from src.infrastructure.db.models.agent import AgentModel
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper


@final
@dataclass(frozen=True, slots=True)
class AgentDBMapper:
    _queue_db_mapper: QueueDBMapper

    @staticmethod
    def to_entity(model: AgentModel) -> Agent:
        return Agent(
            agent_uuid=model.agent_uuid,
            agent_name=model.agent_name,
            agent_number=AgentNumber(model.agent_number),
            agent_password=model.agent_password,
            domain_uuid=model.domain_uuid,
            user_uuid=model.user_uuid,
            agent_status=model.agent_status,
        )

    @staticmethod
    def to_model(entity: Agent) -> AgentModel:
        return AgentModel(
            agent_uuid=entity.agent_uuid,
            agent_name=entity.agent_name,
            agent_number=entity.agent_number.value,
            agent_password=entity.agent_password,
            domain_uuid=entity.domain_uuid,
            user_uuid=entity.user_uuid,
            agent_status=entity.agent_status,
        )

    def to_dto(self, model: AgentModel) -> AgentDTO:
        queues = [self._queue_db_mapper.to_dto(tier.queue) for tier in model.tiers]
        return AgentDTO(
            agent_uuid=model.agent_uuid,
            agent_name=model.agent_name,
            agent_number=model.agent_number,
            agent_password=model.agent_password,
            domain_uuid=model.domain_uuid,
            agent_status=model.agent_status,
            queues=queues,
        )

    @staticmethod
    def update_model_from_entity(model: AgentModel, entity: Agent) -> None:
        model.agent_uuid = entity.agent_uuid
        model.agent_name = entity.agent_name
        model.agent_number = entity.agent_number.value
        model.agent_password = entity.agent_password
        model.domain_uuid = entity.domain_uuid
