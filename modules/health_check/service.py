"""
Health Check Module Service
This module can be extended independently for health check functionality.
"""

from typing import Dict, Any
from app.services.system_metrics import SystemMetricsService


class HealthCheckModule:
    """
    Health check module service.
    Wraps system metrics service for module-specific functionality.
    """
    
    def __init__(self):
        self.metrics_service = SystemMetricsService()
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status.
        Can be extended with module-specific health checks.
        """
        metrics = self.metrics_service.get_all_metrics()
        
        # Add module-specific health assessment
        health_status = self._assess_health(metrics)
        
        return {
            **metrics,
            "health_status": health_status
        }
    
    def _assess_health(self, metrics: Dict[str, Any]) -> str:
        """
        Assess overall health based on metrics.
        Returns: 'healthy', 'degraded', or 'unhealthy'
        """
        # Simple health assessment logic
        cpu_usage = metrics.get("cpu", {}).get("usage_percent", 0)
        memory_percent = metrics.get("memory", {}).get("percent", 0)
        temp = metrics.get("temperature", {}).get("celsius")
        voltage_status = metrics.get("voltage", {}).get("status", "N/A")
        
        # Check for critical issues
        if voltage_status == "WARNING":
            return "degraded"
        
        if temp and temp > 80:  # High temperature threshold
            return "degraded"
        
        if cpu_usage > 95 or memory_percent > 95:
            return "degraded"
        
        return "healthy"


