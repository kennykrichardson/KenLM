from pydantic import BaseModel, Field, field_validator


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    system: str = Field(
        default="You are a concise, helpful assistant. Follow the user's instruction.",
        max_length=1000,
    )
    max_tokens: int = Field(default=160, ge=1, le=256)
    temperature: float = Field(default=0.45, ge=0.0, le=1.5)
    stop: list[str] | None = Field(default=None, max_length=4)

    @field_validator("stop")
    @classmethod
    def validate_stop(cls, value):
        if value is not None and any(len(item) > 80 for item in value):
            raise ValueError("Stop sequences must be 80 characters or fewer.")
        return value


class ChatMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=4000)

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if value not in {"system", "user", "assistant"}:
            raise ValueError("role must be system, user, or assistant")
        return value


class ChatCompletionRequest(BaseModel):
    model: str = "kennylm-small"
    messages: list[ChatMessage] = Field(min_length=1, max_length=12)
    max_tokens: int = Field(default=160, ge=1, le=256)
    temperature: float = Field(default=0.45, ge=0.0, le=1.5)
    stream: bool = False
