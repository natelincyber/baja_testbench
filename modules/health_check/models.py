"""
Health Check Module Models
Module-specific data models.
"""

from pydantic import BaseModel
from typing import Literal


class HealthStatus(BaseModel):
    """Health status assessment."""
    status: Literal["healthy", "degraded", "unhealthy"]
    message: str = ""


