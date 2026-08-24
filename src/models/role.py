from typing import List
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.annotations import int_pk, tz_timestamp


class Role(Base):
    """Role configuration entity allowing granular features permissions."""
    __tablename__ = "roles"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    permissions: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")

    created_at: Mapped[tz_timestamp]

    users: Mapped[List["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles"
    )
