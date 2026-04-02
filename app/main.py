from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers.agent import router as agent_router
from app.routers.brand_identity import router as brand_identity_router
from app.routers.clients import router as clients_router
from app.routers.health import router as health_router


app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(agent_router)
app.include_router(clients_router, tags=["clients"])
app.include_router(brand_identity_router, tags=["brand-identity"])

uploads_dir = Path(settings.UPLOAD_DIR)
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
