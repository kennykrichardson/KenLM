import secrets
from fastapi import Header, HTTPException
from app.config import get_settings


async def require_api_key(authorization: str | None = Header(default=None)):
    expected = get_settings().api_key
    # An empty key is convenient for local development. Set KENNYLM_API_KEY
    # in Render before exposing the service publicly.
    if not expected:
        return
    supplied = ""
    if authorization and authorization.lower().startswith("bearer "):
        supplied = authorization[7:].strip()
    if not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
