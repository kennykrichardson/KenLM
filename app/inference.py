from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any

import httpx
from llama_cpp import Llama

from app.config import get_settings


class InferenceEngine:
    def __init__(self) -> None:
        self._model: Llama | None = None
        self._lock = threading.Lock()

    def load(self) -> None:
        settings = get_settings()
        model_path = Path(settings.model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)

        if not model_path.exists():
            self._download_model(model_path)

        self._model = Llama(
            model_path=str(model_path),
            n_ctx=settings.context_size,
            n_threads=settings.model_threads,
            n_batch=64,
            use_mmap=True,
            use_mlock=False,
            verbose=False,
        )

    @staticmethod
    def _download_model(destination: Path) -> None:
        settings = get_settings()
        temporary = destination.with_suffix(".download")
        headers = {"User-Agent": "KennyLM/0.1"}
        with httpx.stream(
            "GET",
            settings.model_url,
            follow_redirects=True,
            timeout=httpx.Timeout(60.0, read=180.0),
            headers=headers,
        ) as response:
            response.raise_for_status()
            with temporary.open("wb") as output:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)
        temporary.replace(destination)

    def generate(
        self,
        prompt: str,
        system: str,
        max_tokens: int,
        temperature: float,
        stop: list[str] | None = None,
    ) -> dict[str, Any]:
        if self._model is None:
            raise RuntimeError("The model has not loaded.")
        with self._lock:
            return self._model.create_chat_completion(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop,
            )

    def chat(self, messages: list[dict[str, str]], max_tokens: int, temperature: float):
        if self._model is None:
            raise RuntimeError("The model has not loaded.")
        with self._lock:
            return self._model.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )


engine = InferenceEngine()
