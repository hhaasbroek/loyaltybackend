from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    environment: str
    service: str


@router.get("/health", response_model=HealthCheckResponse, summary="Health Check")
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint for container orchestrators (like Railway) and uptime monitoring.
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        environment=settings.ENVIRONMENT,
        service=settings.PROJECT_NAME,
    )
