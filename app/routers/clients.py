from __future__ import annotations

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, Response, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases import get_db
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.services.client_service import ClientService


router = APIRouter(prefix="/api/clients")


@router.get(
    "",
    response_model=list[ClientResponse],
    summary="Lista clienti",
    description="Restituisce la lista clienti filtrata per stato e ricerca testuale su nome/settore.",
)
async def list_clients(
    status_filter: Literal["active", "archived"] | None = Query(default="active", alias="status"),
    search: str | None = Query(default=None, description="Ricerca per nome o settore"),
    db: AsyncSession = Depends(get_db),
) -> list[ClientResponse]:
    return await ClientService.get_all(db=db, status_filter=status_filter, search=search)


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    summary="Dettaglio cliente",
    description="Recupera un cliente tramite id.",
    responses={404: {"description": "Cliente non trovato"}},
)
async def get_client(client_id: UUID, db: AsyncSession = Depends(get_db)) -> ClientResponse:
    return await ClientService.get_by_id(db=db, client_id=client_id)


@router.post(
    "",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crea cliente",
    description="Crea un nuovo cliente.",
)
async def create_client(data: ClientCreate, db: AsyncSession = Depends(get_db)) -> ClientResponse:
    return await ClientService.create(db=db, data=data)


@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
    summary="Aggiorna cliente",
    description="Aggiorna parzialmente un cliente esistente.",
    responses={404: {"description": "Cliente non trovato"}},
)
async def update_client(
    client_id: UUID,
    data: ClientUpdate,
    db: AsyncSession = Depends(get_db),
) -> ClientResponse:
    return await ClientService.update(db=db, client_id=client_id, data=data)


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Archivia cliente",
    description="Soft delete: imposta status=archived.",
    responses={404: {"description": "Cliente non trovato"}},
)
async def delete_client(client_id: UUID, db: AsyncSession = Depends(get_db)) -> Response:
    await ClientService.delete(db=db, client_id=client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{client_id}/logo",
    summary="Carica logo cliente",
    description="Carica un logo (jpeg/png/webp/svg) fino a 2MB e aggiorna logo_path.",
    responses={
        400: {"description": "Formato non supportato"},
        404: {"description": "Cliente non trovato"},
        413: {"description": "File troppo grande"},
    },
)
async def upload_client_logo(
    client_id: UUID,
    file: UploadFile = File(..., description="File logo"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    logo_path = await ClientService.upload_logo(db=db, client_id=client_id, file=file)
    return {"logo_path": logo_path}
