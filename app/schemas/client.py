from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class ContactItem(BaseModel):
    name: str
    email: EmailStr
    role: str | None = None


class LinkItem(BaseModel):
    url: HttpUrl
    label: str


class ClientCreate(BaseModel):
    name: str
    sector: str | None = None
    website: HttpUrl | None = None
    links: list[LinkItem] = Field(default_factory=list)
    contacts: list[ContactItem] = Field(default_factory=list)
    notes: str | None = None
    status: Literal["active", "archived"] = "active"


class ClientUpdate(BaseModel):
    name: str | None = None
    sector: str | None = None
    website: HttpUrl | None = None
    links: list[LinkItem] | None = None
    contacts: list[ContactItem] | None = None
    notes: str | None = None
    status: Literal["active", "archived"] | None = None


class ClientResponse(BaseModel):
    id: UUID
    name: str
    sector: str | None = None
    website: str | None = None
    links: list[LinkItem]
    contacts: list[ContactItem]
    notes: str | None = None
    logo_path: str | None = None
    status: Literal["active", "archived"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientListResponse(BaseModel):
    items: list[ClientResponse]
    total: int
