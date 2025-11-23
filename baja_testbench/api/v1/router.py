"""
API v1 router aggregation.
"""

from fastapi import APIRouter
from baja_testbench.api.v1 import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])


