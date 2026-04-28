import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models import Base


class NumberModel(Base):
    __tablename__ = 'webgram_numbers'

    number_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    number_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    number_number: Mapped[str] = mapped_column(String(255), nullable=False)
