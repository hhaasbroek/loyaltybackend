from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.firebase import get_firebase_app
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")

    # Initialize Firebase Admin SDK on startup
    try:
        get_firebase_app()
    except Exception as e:
        print(f"Warning: Firebase Admin init failed: {e}")

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }


# Include V1 API Router
app.include_router(api_router, prefix=settings.API_V1_STR)
