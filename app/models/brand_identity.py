from __future__ import annotations

from datetime import datetime
from uuid import UUID as UUIDType
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class BrandIdentity(Base):
    __tablename__ = "brand_identities"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    business_description: Mapped[str] = mapped_column(Text, default="")
    mission: Mapped[str] = mapped_column(Text, default="")
    vision: Mapped[str] = mapped_column(Text, default="")
    unique_value_proposition: Mapped[str] = mapped_column(Text, default="")
    logos: Mapped[list[dict[str, str]]] = mapped_column(JSONB, default=list)
    tone_of_voice: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
    visual_identity: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
    target_audience: Mapped[dict[str, object]] = mapped_column(JSONB, default=dict)
    competitors: Mapped[list[str]] = mapped_column(JSONB, default=list)
    differentiators: Mapped[list[str]] = mapped_column(JSONB, default=list)
    products_services: Mapped[list[str]] = mapped_column(JSONB, default=list)
    keywords_seo: Mapped[list[str]] = mapped_column(JSONB, default=list)
    approved_claims: Mapped[list[str]] = mapped_column(JSONB, default=list)
    restricted_topics: Mapped[list[str]] = mapped_column(JSONB, default=list)
    legal_notes: Mapped[str] = mapped_column(Text, default="")
    cta_primary: Mapped[str] = mapped_column(Text, default="")
    cta_secondary: Mapped[str] = mapped_column(Text, default="")
    preferred_channels: Mapped[list[str]] = mapped_column(JSONB, default=list)
    ai_last_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_last_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
