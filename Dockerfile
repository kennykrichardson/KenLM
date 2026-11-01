FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CMAKE_ARGS="-DGGML_NATIVE=OFF -DGGML_OPENMP=OFF" \
    MODEL_PATH=/opt/kenlm/models/smollm2-135m-instruct-q4_k_m.gguf

WORKDIR /service

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

RUN mkdir -p /opt/kenlm/models \
    && curl -fL --retry 3 \
    "https://huggingface.co/lmstudio-community/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf" \
    -o /opt/kenlm/models/smollm2-135m-instruct-q4_k_m.gguf

COPY app ./app

EXPOSE 10000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1"]