from __future__ import annotations

from pathlib import Path
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    ALLOWED_LOGO_MIME_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/svg+xml": ".svg",
    }
    MAX_LOGO_SIZE_BYTES = 2 * 1024 * 1024

    @staticmethod
    async def get_all(
        db: AsyncSession,
        status_filter: str | None = "active",
        search: str | None = None,
    ) -> list[Client]:
        query = select(Client)

        if status_filter:
            query = query.where(Client.status == status_filter)

        if search:
            term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Client.name.ilike(term),
                    Client.sector.ilike(term),
                )
            )

        query = query.order_by(Client.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, client_id: UUID) -> Client:
        result = await db.execute(select(Client).where(Client.id == client_id))
        client = result.scalar_one_or_none()
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente non trovato",
            )
        return client

    @classmethod
    async def create(cls, db: AsyncSession, data: ClientCreate) -> Client:
        payload = data.model_dump(mode="json")
        client = Client(**payload)
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return client

    @classmethod
    async def update(
        cls,
        db: AsyncSession,
        client_id: UUID,
        data: ClientUpdate,
    ) -> Client:
        client = await cls.get_by_id(db, client_id)
        payload = data.model_dump(exclude_unset=True, mode="json")

        for field, value in payload.items():
            setattr(client, field, value)

        await db.commit()
        await db.refresh(client)
        return client

    @classmethod
    async def delete(cls, db: AsyncSession, client_id: UUID) -> None:
        client = await cls.get_by_id(db, client_id)
        client.status = "archived"
        await db.commit()

    @classmethod
    async def upload_logo(
        cls,
        db: AsyncSession,
        client_id: UUID,
        file: UploadFile,
    ) -> str:
        client = await cls.get_by_id(db, client_id)

        ext = cls.ALLOWED_LOGO_MIME_TYPES.get(file.content_type or "")
        if not ext:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato logo non supportato",
            )

        content = await file.read()
        if len(content) > cls.MAX_LOGO_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Il file supera il limite di 2MB",
            )

        upload_dir = Path(settings.UPLOAD_DIR) / "clients" / str(client_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        logo_filename = f"logo{ext}"
        logo_file_path = upload_dir / logo_filename
        logo_file_path.write_bytes(content)

        logo_path = f"/uploads/clients/{client_id}/{logo_filename}"
        client.logo_path = logo_path

        await db.commit()
        await db.refresh(client)
        return logo_path
