from fastapi import APIRouter

from models.health_model import HealthResponse
from utils.config import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get(
    "",
    response_model=HealthResponse,
    summary="Application Health Check"
)
async def health_check():
    """
    Simple endpoint to verify that the backend is running.
    """

    return HealthResponse(
        status="Healthy",
        version=settings.APP_VERSION,
        application=settings.APP_NAME
    )