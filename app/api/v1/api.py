from fastapi import APIRouter
from app.api.v1.endpoints import health, cards

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(cards.router, prefix="/cards", tags=["Cards"])
