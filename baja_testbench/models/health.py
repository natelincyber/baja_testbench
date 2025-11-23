"""
Pydantic models for health check endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class SystemInfo(BaseModel):
    """System platform information."""
    platform: str
    platform_release: str
    platform_version: str
    architecture: str
    hostname: str


class CPUInfo(BaseModel):
    """CPU usage and frequency information."""
    usage_percent: float = Field(..., ge=0, le=100)
    count: int
    frequency_mhz: Optional[float] = None
    frequency_min_mhz: Optional[float] = None
    frequency_max_mhz: Optional[float] = None


class MemoryInfo(BaseModel):
    """Memory (RAM) usage information."""
    total_bytes: int
    available_bytes: int
    used_bytes: int
    percent: float = Field(..., ge=0, le=100)
    total_mb: float
    available_mb: float
    used_mb: float


class TemperatureInfo(BaseModel):
    """CPU temperature information."""
    raw: str
    celsius: Optional[float] = None
    available: bool


class VoltageInfo(BaseModel):
    """Voltage and throttling status information."""
    raw: str
    hex_value: Optional[str] = None
    flags: Optional[Dict[str, bool]] = None
    status: str
    available: bool


class NetworkInfo(BaseModel):
    """Network I/O statistics."""
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int
    mbps_sent: float
    mbps_recv: float


class DiskRootInfo(BaseModel):
    """Disk root partition information."""
    total_bytes: int
    used_bytes: int
    free_bytes: int
    percent: float = Field(..., ge=0, le=100)
    total_gb: float
    used_gb: float
    free_gb: float


class DiskIOInfo(BaseModel):
    """Disk I/O statistics."""
    read_bytes: int
    write_bytes: int
    read_count: int
    write_count: int


class DiskInfo(BaseModel):
    """Disk usage and I/O information."""
    root: DiskRootInfo
    io: Optional[DiskIOInfo] = None


class HealthResponse(BaseModel):
    """Complete health check response."""
    system: SystemInfo
    cpu: CPUInfo
    memory: MemoryInfo
    temperature: TemperatureInfo
    voltage: VoltageInfo
    network: NetworkInfo
    disk: DiskInfo


