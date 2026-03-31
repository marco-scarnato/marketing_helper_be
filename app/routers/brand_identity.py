from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases import get_db
from app.schemas.brand_identity import (
    AIBrandPromptRequest,
    AIBrandPromptResponse,
    BrandIdentityCreate,
    BrandIdentityResponse,
    BrandIdentityUpdate,
)
from app.services.brand_identity_service import BrandIdentityService


router = APIRouter(prefix="/api/clients")


@router.get(
    "/{client_id}/brand-identity",
    response_model=BrandIdentityResponse,
    summary="Recupera brand identity",
)
async def get_brand_identity(client_id: UUID, db: AsyncSession = Depends(get_db)) -> BrandIdentityResponse:
    brand_identity = await BrandIdentityService.get_by_client(db, client_id)
    if brand_identity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand identity non trovata")
    return brand_identity


@router.post(
    "/{client_id}/brand-identity",
    response_model=BrandIdentityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crea brand identity",
)
async def create_brand_identity(
    client_id: UUID,
    data: BrandIdentityCreate,
    db: AsyncSession = Depends(get_db),
) -> BrandIdentityResponse:
    existing = await BrandIdentityService.get_by_client(db, client_id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Brand identity già presente per questo cliente",
        )

    if data.client_id != client_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="client_id nel body non coincide con la route",
        )

    return await BrandIdentityService.create(db, data)


@router.patch(
    "/{client_id}/brand-identity",
    response_model=BrandIdentityResponse,
    summary="Aggiorna brand identity",
)
async def update_brand_identity(
    client_id: UUID,
    data: BrandIdentityUpdate,
    db: AsyncSession = Depends(get_db),
) -> BrandIdentityResponse:
    if data.client_id != client_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="client_id nel body non coincide con la route",
        )

    try:
        return await BrandIdentityService.update(db, client_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/{client_id}/brand-identity/logos",
    response_model=BrandIdentityResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload logo asset brand identity",
)
async def upload_brand_identity_logo_asset(
    client_id: UUID,
    file: UploadFile = File(...),
    variant: str = Form("icon"),
    db: AsyncSession = Depends(get_db),
) -> BrandIdentityResponse:
    brand_identity = await BrandIdentityService.get_by_client(db, client_id)
    if brand_identity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand identity non trovata")

    try:
        path = await BrandIdentityService.upload_logo_asset(client_id, file)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except OverflowError as exc:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(exc)) from exc

    try:
        return await BrandIdentityService.add_logo_asset(db, client_id, path, variant)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/{client_id}/brand-identity/ai-generate",
    response_model=AIBrandPromptResponse,
    status_code=status.HTTP_200_OK,
    summary="Genera proposta AI per sezione",
)
async def ai_generate_brand_identity_section(
    client_id: UUID,
    data: AIBrandPromptRequest,
) -> AIBrandPromptResponse:
    if data.client_id != client_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="client_id nel body non coincide con la route",
        )

    return await BrandIdentityService.ai_generate_section(client_id, data.prompt, data.section)
