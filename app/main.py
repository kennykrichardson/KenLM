from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.inference import engine
from app.routes import generate, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = engine
    app.state.model_loaded = False
    engine.load()
    app.state.model_loaded = True
    yield
    app.state.model_loaded = False


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A small, self-hosted text-generation API powered by a local GGUF model.",
    lifespan=lifespan,
)

origins = [item.strip() for item in settings.cors_origins.split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if origins == ["*"] else origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(health.router)
app.include_router(generate.router)
