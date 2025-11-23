"""
Health check API endpoints.
"""

from fastapi import APIRouter, Depends
from app.models.health import HealthResponse
from app.services.system_metrics import SystemMetricsService
from app.api.deps import get_metrics_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health(
    metrics_service: SystemMetricsService = Depends(get_metrics_service)
) -> HealthResponse:
    """
    Returns comprehensive system health metrics.
    
    Includes:
    - CPU usage and frequency
    - RAM usage
    - CPU temperature (Raspberry Pi specific)
    - Voltage/throttling status (Raspberry Pi specific)
    - Network statistics
    - Disk usage and I/O
    """
    metrics = metrics_service.get_all_metrics()
    return HealthResponse(**metrics)


