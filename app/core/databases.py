from collections.abc import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


engine = create_async_engine(settings.POSTGRES_URL, future=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db: AsyncIOMotorDatabase = mongo_client[settings.MONGO_DB_NAME]


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def get_mongo_db() -> AsyncIOMotorDatabase:
    return mongo_db
