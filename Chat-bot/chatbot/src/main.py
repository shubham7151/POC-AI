from fastapi import FastAPI
from src.api.router.router import router
from src.model.models import Base
from contextlib import asynccontextmanager
from src.db.repository import Database
from src.core.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_config = {
        'DATABASE_URL': settings.DATABASE_URL
    }
    Base.metadata.create_all(bind=Database(db_config=db_config).engine)
    yield

app = FastAPI(
    title="Simple Chatbot",
    description="A simple chatbot using Google Generative AI",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

