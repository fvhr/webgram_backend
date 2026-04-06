import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models import Base


class ExtensionModel(Base):
    __tablename__ = 'webgram_extensions'

    extension_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    extension_number: Mapped[str] = mapped_column(String(255), nullable=False)
    extension_password: Mapped[str] = mapped_column(String(255), nullable=True)
    caller_id_name: Mapped[str] = mapped_column(String(255), nullable=True)
    caller_id_number: Mapped[str] = mapped_column(String(255), nullable=True)
    domain_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                   ForeignKey('webgram_domains.domain_uuid'),
                                                   nullable=False)
