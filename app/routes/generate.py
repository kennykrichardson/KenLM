import time
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from app.schemas import GenerateRequest, ChatCompletionRequest
from app.security import require_api_key

router = APIRouter(prefix="/v1", tags=["inference"], dependencies=[Depends(require_api_key)])


@router.get("/models")
async def models():
    return {
        "object": "list",
        "data": [{
            "id": "kennylm-small",
            "object": "model",
            "owned_by": "kennyrichardson",
        }],
    }


@router.post("/generate")
async def generate(payload: GenerateRequest, request: Request):
    if not request.app.state.model_loaded:
        raise HTTPException(status_code=503, detail="Model is still loading.")
    try:
        result = await run_in_threadpool(
            request.app.state.engine.generate,
            payload.prompt,
            payload.system,
            payload.max_tokens,
            payload.temperature,
            payload.stop,
        )
        choice = result["choices"][0]
        return {
            "text": choice["message"]["content"].strip(),
            "model": "kennylm-small",
            "usage": result.get("usage", {}),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {type(exc).__name__}") from exc


@router.post("/chat/completions")
async def chat_completions(payload: ChatCompletionRequest, request: Request):
    if payload.stream:
        raise HTTPException(status_code=400, detail="Streaming is not enabled on the free-tier build.")
    if not request.app.state.model_loaded:
        raise HTTPException(status_code=503, detail="Model is still loading.")
    try:
        messages = [message.model_dump() for message in payload.messages]
        result = await run_in_threadpool(
            request.app.state.engine.chat,
            messages,
            payload.max_tokens,
            payload.temperature,
        )
        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:16]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "kennylm-small",
            "choices": [{
                "index": 0,
                "message": result["choices"][0]["message"],
                "finish_reason": result["choices"][0].get("finish_reason", "stop"),
            }],
            "usage": result.get("usage", {}),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {type(exc).__name__}") from exc
