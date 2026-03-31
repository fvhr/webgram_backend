import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models import Base


class RoleModel(Base):
    __tablename__ = 'webgram_roles'

    role_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    role_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    users = relationship('UserModel', back_populates='role', lazy='selectin')
