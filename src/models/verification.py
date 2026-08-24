import uuid
from typing import Optional
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.annotations import int_pk, tz_timestamp


class UserVerification(Base):
    """Handles multiple delivery channels verification logic for users."""
    __tablename__ = "user_verifications"

    id: Mapped[int_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    channel: Mapped[str] = mapped_column(String(50), nullable=False)

    destination: Mapped[str] = mapped_column(String(255), nullable=False)

    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

    verification_value: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    last_sent_at: Mapped[Optional[tz_timestamp]] = mapped_column(default=None, server_default=None)
    expires_at: Mapped[Optional[tz_timestamp]] = mapped_column(default=None, server_default=None)

    created_at: Mapped[tz_timestamp]

    user: Mapped["User"] = relationship(back_populates="verifications")

    __table_args__ = (
        UniqueConstraint("user_id", "channel", name="uq_user_channel"),
    )
