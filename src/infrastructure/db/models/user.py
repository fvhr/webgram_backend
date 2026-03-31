import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models import Base


class UserModel(Base):
    __tablename__ = 'webgram_users'

    user_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_password: Mapped[str] = mapped_column(String(500), nullable=False)
    role_uuid: Mapped[uuid.UUID] = mapped_column(UUID,
                                                 ForeignKey('webgram_roles.role_uuid'),
                                                 nullable=False)

    role = relationship('RoleModel', back_populates='users', lazy='selectin')
