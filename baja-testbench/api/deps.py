"""
FastAPI dependencies for dependency injection.
"""

from app.services.system_metrics import SystemMetricsService


def get_metrics_service() -> SystemMetricsService:
    """Dependency to get system metrics service instance."""
    return SystemMetricsService()


