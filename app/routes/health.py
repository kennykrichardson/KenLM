from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(request: Request):
    loaded = getattr(request.app.state, "model_loaded", False)
    return {
        "status": "ok" if loaded else "loading",
        "model_loaded": loaded,
        "service": "KennyLM",
    }


@router.get("/")
async def root():
    return {
        "name": "KennyLM",
        "description": "A tiny self-hosted language model API.",
        "docs": "/docs",
        "health": "/health",
    }
