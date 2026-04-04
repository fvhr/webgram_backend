import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models import Base


class AgentModel(Base):
    __tablename__ = 'webgram_agents'

    agent_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    agent_name: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_number: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_password: Mapped[str] = mapped_column(String(255), nullable=False)
    domain_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                 ForeignKey('webgram_domains.domain_uuid'),
                                                 nullable=False)
    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                 ForeignKey('webgram_users.user_uuid'),
                                                 nullable=False)
    agent_status: Mapped[str] = mapped_column(String(255), nullable=False)
