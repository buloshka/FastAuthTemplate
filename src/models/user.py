import uuid
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.annotations import uuid_pk, tz_timestamp


class UserRoleAssociation(Base):
    """Many-to-Many association table linking Users and Roles."""
    __tablename__ = 'user_roles'

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)


class User(Base):
    """Core User entity configuration."""
    __tablename__ = 'users'

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, server_default='true')
    created_at: Mapped[tz_timestamp]

    roles: Mapped[List["Role"]] = relationship(
        secondary="user_roles",
        back_populates="users",
        lazy="selectin"
    )

    verifications: Mapped[List["UserVerification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
