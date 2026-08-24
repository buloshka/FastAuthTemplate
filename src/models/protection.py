import uuid
from typing import Optional
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.annotations import bigint_pk, tz_timestamp


class SecurityAuditLog(Base):
    """Persistent matrix tracking security critical gateway and infrastructure events."""
    __tablename__ = "security_audit_logs"

    id: Mapped[bigint_pk]
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False,
                                            index=True)  # "login_failed", "token_compromised"
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=False)
    device_fingerprint: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")
    created_at: Mapped[tz_timestamp]


class UserActivityLog(Base):
    """Audit trail monitoring internal business actions executed by verified accounts."""
    __tablename__ = "user_activity_logs"

    id: Mapped[bigint_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    http_method: Mapped[str] = mapped_column(String(10), nullable=False)
    request_path: Mapped[str] = mapped_column(String(255), nullable=False)

    # {"before": {...}, "after": {...}}
    details: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")

    created_at: Mapped[tz_timestamp]
