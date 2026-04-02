from __future__ import annotations

import httpx

from app.core.config import settings
from app.schemas.agent import AgentInvokeRequest, AgentInvokeResponse


class AgentGatewayError(Exception):
    pass


class AgentService:
    @staticmethod
    async def invoke(payload: AgentInvokeRequest) -> AgentInvokeResponse:
        url = f"{settings.AGENT_URL}/agent/invoke"
        timeout = httpx.Timeout(settings.AGENT_TIMEOUT_SECONDS)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=payload.model_dump(mode="json"))
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise AgentGatewayError("Servizio agent non disponibile") from exc

        return AgentInvokeResponse.model_validate(response.json())
