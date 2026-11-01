# 🤖 KenLM

**A lightweight, self-hosted language model API.**

KenLM is a compact AI inference service built with **FastAPI** and **llama.cpp**. It provides HTTP endpoints that allow applications to interact with a locally hosted language model without depending on paid external AI APIs.

The initial deployment uses **SmolLM2-135M-Instruct**, quantized in GGUF format.

## ✨ Features

- ⚡ Lightweight language model inference
- 🚀 FastAPI-powered REST API
- 🧠 GGUF model support through llama.cpp
- 🔐 Bearer-token API authentication
- 💬 Chat completions endpoint
- 📝 Text generation endpoint
- 📖 Interactive API documentation
- 🐳 Docker-based deployment
- ☁️ Render deployment configuration

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| FastAPI | API framework |
| llama.cpp | Model inference |
| llama-cpp-python | Python model integration |
| Pydantic | Configuration and validation |
| Docker | Containerization |
| Render | Hosting |

## 📁 Project Structure

```text
KenLM/
├── app/
│   ├── routes/
│   │   ├── generate.py
│   │   └── health.py
│   ├── config.py
│   ├── inference.py
│   ├── main.py
│   ├── schemas.py
│   └── security.py
├── .env.example
├── .gitignore
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kennykrichardson/KenLM.git
cd KenLM
```

### 2. Create a virtual environment

```bash
python -m venv .kenlm
```

Activate it:

**Windows**
```powershell
.kenlm\Scripts\activate
```

**Linux / macOS**
```bash
source .kenlm/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure your settings.

```env
KENLM_API_KEY=
MODEL_PATH=./models/smollm2-135m-instruct-q4_k_m.gguf
CONTEXT_SIZE=512
MAX_TOKENS=160
MODEL_THREADS=1
```

For local development, the model is downloaded if it is not already present at the configured path.

### 5. Start the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access the API documentation:

```text
http://localhost:8000/docs
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Service information |
| `/health` | GET | Health status |
| `/v1/models` | GET | Available model |
| `/v1/generate` | POST | Generate text |
| `/v1/chat/completions` | POST | Chat completions |
| `/docs` | GET | Interactive API documentation |

Protected endpoints require a Bearer token when API authentication is configured.

### Example request

```bash
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "Explain artificial intelligence",
    "max_tokens": 100
  }'
```

## 🐳 Docker Deployment

Build the Docker image:

```bash
docker build -t kenlm .
```

Run the container:

```bash
docker run -p 8000:8000 kenlm
```

## ☁️ Render Deployment

KenLM includes a `render.yaml` Blueprint configuration.

1. Push the repository to GitHub.
2. Connect GitHub to Render.
3. Create a new Blueprint.
4. Select the KenLM repository.
5. Apply the configuration.
6. Wait for the Docker build and deployment.

Render's free resources are limited. Cold starts, memory constraints and slow inference are expected possibilities.

## ⚙️ Initial Model

**SmolLM2-135M-Instruct**

- Format: GGUF
- Quantization: Q4_K_M
- Runtime: llama.cpp
- Context size: 512 tokens by default

The initial model is intentionally small to explore low-cost inference hosting. Its capabilities are limited compared with larger language models.

## 🔒 Security

- Configure an API key for protected endpoints.
- Never expose private API keys in frontend code.
- Configure CORS appropriately for production.
- Avoid committing `.env` files or secrets.

## 📌 Project Status

**Experimental / Initial Deployment**

KenLM is an evolving project. Performance, resource usage and deployment reliability will depend on the selected model and hosting environment.

## 👨‍💻 Author

**Kenny Richardson**

- GitHub: [@kennykrichardson](https://github.com/kennykrichardson)
- Portfolio: [kennykrichardson-ai.onrender.com](https://kennykrichardson-ai.onrender.com)

---

<p align="center">
  Built with Python, FastAPI and a little ambition. 🤖
</p>