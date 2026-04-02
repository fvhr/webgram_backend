import uuid

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models import Base


class DomainModel(Base):
    __tablename__ = 'webgram_domains'

    domain_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    domain_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    domain_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    domain_description: Mapped[str] = mapped_column(String(255), nullable=True)
