from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.agent import AgentInvokeRequest, AgentInvokeResponse
from app.services.agent_service import AgentGatewayError, AgentService


router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post(
    "/invoke",
    response_model=AgentInvokeResponse,
    status_code=status.HTTP_200_OK,
    summary="Invoca workflow agent",
)
async def invoke_agent(payload: AgentInvokeRequest) -> AgentInvokeResponse:
    try:
        return await AgentService.invoke(payload)
    except AgentGatewayError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
