import uuid

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infrastructure.db.models import Base


class TierModel(Base):
    __tablename__ = 'webgram_tiers'

    tier_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    agent_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                  ForeignKey('webgram_agents.agent_uuid'),
                                                  nullable=False)
    queue_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                  ForeignKey('webgram_queues.queue_uuid'),
                                                  nullable=False)

    queue = relationship('QueueModel', back_populates='tiers', lazy='selectin')
    agent = relationship('AgentModel', back_populates='tiers', lazy='selectin')
