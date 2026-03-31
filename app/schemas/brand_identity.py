from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ToneOfVoice(BaseModel):
    style: str = ""
    language: str = ""
    do_say: list[str] = Field(default_factory=list)
    dont_say: list[str] = Field(default_factory=list)


class VisualIdentity(BaseModel):
    color_palette: list[str] = Field(default_factory=list)
    typography: str = ""
    imagery_style: str = ""
    logo_usage_notes: str = ""


class CustomerProfile(BaseModel):
    demographics: str = ""
    psychographics: str = ""
    pain_points: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    buying_triggers: list[str] = Field(default_factory=list)


class LogoAsset(BaseModel):
    path: str
    variant: Literal["icon", "horizontal", "negative", "positive"]
    uploaded_at: str | None = None


class BrandIdentityCreate(BaseModel):
    client_id: UUID
    business_description: str = ""
    mission: str = ""
    vision: str = ""
    unique_value_proposition: str = ""
    tone_of_voice: ToneOfVoice = Field(default_factory=ToneOfVoice)
    visual_identity: VisualIdentity = Field(default_factory=VisualIdentity)
    target_audience: CustomerProfile = Field(default_factory=CustomerProfile)
    competitors: list[str] = Field(default_factory=list)
    differentiators: list[str] = Field(default_factory=list)
    products_services: list[str] = Field(default_factory=list)
    keywords_seo: list[str] = Field(default_factory=list)
    approved_claims: list[str] = Field(default_factory=list)
    restricted_topics: list[str] = Field(default_factory=list)
    legal_notes: str = ""
    cta_primary: str = ""
    cta_secondary: str = ""
    preferred_channels: list[str] = Field(default_factory=list)
    logos: list[LogoAsset] = Field(default_factory=list)


class BrandIdentityUpdate(BaseModel):
    client_id: UUID
    business_description: str | None = None
    mission: str | None = None
    vision: str | None = None
    unique_value_proposition: str | None = None
    tone_of_voice: ToneOfVoice | None = None
    visual_identity: VisualIdentity | None = None
    target_audience: CustomerProfile | None = None
    competitors: list[str] | None = None
    differentiators: list[str] | None = None
    products_services: list[str] | None = None
    keywords_seo: list[str] | None = None
    approved_claims: list[str] | None = None
    restricted_topics: list[str] | None = None
    legal_notes: str | None = None
    cta_primary: str | None = None
    cta_secondary: str | None = None
    preferred_channels: list[str] | None = None
    logos: list[LogoAsset] | None = None


class BrandIdentityResponse(BaseModel):
    id: UUID
    client_id: UUID
    business_description: str
    mission: str
    vision: str
    unique_value_proposition: str
    tone_of_voice: ToneOfVoice
    visual_identity: VisualIdentity
    target_audience: CustomerProfile
    competitors: list[str]
    differentiators: list[str]
    products_services: list[str]
    keywords_seo: list[str]
    approved_claims: list[str]
    restricted_topics: list[str]
    legal_notes: str
    cta_primary: str
    cta_secondary: str
    preferred_channels: list[str]
    logos: list[LogoAsset]
    ai_last_prompt: str | None = None
    ai_last_response: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AIBrandPromptRequest(BaseModel):
    client_id: UUID
    prompt: str
    section: str


class AIBrandPromptResponse(BaseModel):
    section: str
    proposed: dict[str, Any]
    reasoning: str
