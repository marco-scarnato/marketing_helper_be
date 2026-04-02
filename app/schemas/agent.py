from __future__ import annotations

from pydantic import BaseModel, Field


class AgentInvokeRequest(BaseModel):
    client_id: str = Field(..., description="ID del cliente")
    objective: str = Field(..., description="Obiettivo del task da eseguire")
    context: dict[str, str] = Field(default_factory=dict, description="Contesto opzionale")


class AgentInvokeResponse(BaseModel):
    client_id: str
    objective: str
    output: str
    steps: list[str]
    model: str
