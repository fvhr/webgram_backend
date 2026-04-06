import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models import Base


class QueueModel(Base):
    __tablename__ = 'webgram_queues'

    queue_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    queue_name: Mapped[str] = mapped_column(String(255), nullable=False)
    queue_number: Mapped[str] = mapped_column(String(255), nullable=False)
    domain_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                   ForeignKey('webgram_domains.domain_uuid'),
                                                   nullable=False)
