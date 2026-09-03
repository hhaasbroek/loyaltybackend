# Loyalty Backend (FastAPI)

A lightweight, scalable FastAPI backend structured for seamless deployment on [Railway](https://railway.app/).

---

## 🚀 Features

- **FastAPI**: Modern, fast web framework for building APIs with Python.
- **Pydantic v2 & Pydantic Settings**: Strongly typed environment configuration management.
- **Health Check Endpoint**: Ready for container orchestrator liveness/readiness probes (`/api/v1/health`).
- **Production Container Ready**: Optimized `Dockerfile`, `Procfile`, and `railway.json` for Railway deployment.
- **Interactive OpenAPI Documentation**: Built-in Swagger UI at `/docs` and ReDoc at `/redoc`.

---

## 📁 Project Structure

```text
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── health.py    # Health check route
│   │       └── api.py           # V1 API Router aggregation
│   ├── core/
│   │   └── config.py            # Pydantic environment configuration
│   └── main.py                  # FastAPI application entrypoint
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore file
├── Dockerfile                   # Railway Docker configuration
├── Procfile                     # Alternative command declaration
├── railway.json                 # Railway service deployment manifest
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🛠 Local Development Setup

### 1. Prerequisites

- Python 3.10+ (Recommended: Python 3.11 or 3.12)

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Copy the example environment file to `.env`:

```bash
cp .env.example .env
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

Open your browser and navigate to:
- API Root: [http://localhost:8000/](http://localhost:8000/)
- Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🚆 Deploying to Railway

### Method A: Deploying via GitHub (Recommended)

1. Push this repository to GitHub.
2. Log into [Railway.app](https://railway.app/) and create a new project.
3. Select **Deploy from GitHub repo** and choose your repository.
4. Railway will automatically detect the `Dockerfile` or `railway.json`.
5. (Optional) Set environment variables in the Railway Dashboard under the **Variables** tab (e.g. `ENVIRONMENT=production`).
6. Generate a public domain under **Settings > Networking > Public Networking**.

### Method B: Deploying via Railway CLI

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```
2. Login and link project:
   ```bash
   railway login
   railway init
   ```
3. Deploy directly:
   ```bash
   railway up
   ```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `PROJECT_NAME` | `"Loyalty Backend"` | Name displayed in docs |
| `ENVIRONMENT` | `"development"` | Application environment (`development`, `production`) |
| `API_V1_STR` | `"/api/v1"` | Base path prefix for API v1 |
| `PORT` | `8000` | Port for server binding (Railway auto-populates `$PORT`) |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins (JSON array or comma-separated list) |
