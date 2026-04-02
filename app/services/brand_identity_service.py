from __future__ import annotations

import logging
from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.brand_identity import BrandIdentity
from app.schemas.agent import AgentInvokeRequest
from app.schemas.brand_identity import AIBrandPromptResponse, BrandIdentityCreate, BrandIdentityUpdate
from app.services.agent_service import AgentGatewayError, AgentService

logger = logging.getLogger(__name__)


class BrandIdentityService:
    ALLOWED_MIME_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/svg+xml": ".svg",
    }
    MAX_LOGO_SIZE_BYTES = 2 * 1024 * 1024

    @staticmethod
    async def get_by_client(db: AsyncSession, client_id: UUID) -> BrandIdentity | None:
        result = await db.execute(select(BrandIdentity).where(BrandIdentity.client_id == client_id))
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, db: AsyncSession, data: BrandIdentityCreate) -> BrandIdentity:
        payload = data.model_dump(mode="json")
        brand_identity = BrandIdentity(**payload)
        db.add(brand_identity)
        await db.commit()
        await db.refresh(brand_identity)
        return brand_identity

    @classmethod
    async def update(
        cls,
        db: AsyncSession,
        client_id: UUID,
        data: BrandIdentityUpdate,
    ) -> BrandIdentity:
        brand_identity = await cls.get_by_client(db, client_id)
        if brand_identity is None:
            raise ValueError("Brand identity non trovata")

        payload = data.model_dump(exclude_unset=True, mode="json")
        payload.pop("client_id", None)

        for field, value in payload.items():
            setattr(brand_identity, field, value)

        await db.commit()
        await db.refresh(brand_identity)
        return brand_identity

    @classmethod
    async def upload_logo_asset(cls, client_id: UUID, file: UploadFile) -> str:
        ext = cls.ALLOWED_MIME_TYPES.get(file.content_type or "")
        if not ext:
            raise ValueError("Formato logo non supportato")

        content = await file.read()
        if len(content) > cls.MAX_LOGO_SIZE_BYTES:
            raise OverflowError("Il file supera il limite di 2MB")

        uploads_dir = Path(settings.UPLOAD_DIR) / "clients" / str(client_id) / "logos"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        filename = file.filename or f"logo{ext}"
        safe_name = Path(filename).stem.replace(" ", "_")
        final_name = f"{safe_name}{ext}"
        file_path = uploads_dir / final_name
        file_path.write_bytes(content)

        return f"/uploads/clients/{client_id}/logos/{final_name}"

    @classmethod
    async def add_logo_asset(
        cls,
        db: AsyncSession,
        client_id: UUID,
        logo_path: str,
        variant: str,
    ) -> BrandIdentity:
        brand_identity = await cls.get_by_client(db, client_id)
        if brand_identity is None:
            raise ValueError("Brand identity non trovata")

        logos = list(brand_identity.logos or [])
        logos.append({"path": logo_path, "variant": variant})
        brand_identity.logos = logos

        await db.commit()
        await db.refresh(brand_identity)
        return brand_identity

    @staticmethod
    async def ai_generate_section(client_id: UUID, prompt: str, section: str) -> AIBrandPromptResponse:
        logger.info("ai_generate_section called client_id=%s section=%s", client_id, section)

        reasoning_text = "[MVP] Nessun reasoning disponibile"
        try:
            agent_response = await AgentService.invoke(
                AgentInvokeRequest(
                    client_id=str(client_id),
                    objective=prompt,
                    context={"section": section},
                )
            )
            reasoning_text = agent_response.output
        except AgentGatewayError:
            logger.warning("Agent gateway non disponibile, uso fallback reasoning")

        proposed_map: dict[str, dict[str, object]] = {
            "core": {
                "business_description": "Azienda specializzata in soluzioni digitali orientate alla crescita.",
                "mission": "Aiutare le PMI a trasformare obiettivi in risultati misurabili.",
                "vision": "Diventare partner di riferimento per innovazione e performance.",
                "unique_value_proposition": "Metodo data-driven, execution rapida e visione strategica.",
            },
            "tone_of_voice": {
                "tone_of_voice": {
                    "style": "Professionale ma accessibile",
                    "language": "Italiano",
                    "do_say": ["Parliamo di risultati", "Facciamo semplice il complesso"],
                    "dont_say": ["Promesse vaghe", "Gergo troppo tecnico"],
                }
            },
            "full-brand": {
                "business_description": "Brand orientato all'impatto con approccio consulenziale.",
                "mission": "Creare valore concreto con strategie sostenibili.",
                "keywords_seo": ["strategia digitale", "branding", "contenuti"],
            },
        }

        return AIBrandPromptResponse(
            section=section,
            proposed=proposed_map.get(section, {}),
            reasoning=reasoning_text,
        )
