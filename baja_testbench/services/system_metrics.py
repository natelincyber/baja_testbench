"""
Service for collecting system metrics.
Separates business logic from API endpoints.
"""

import psutil
import subprocess
import platform
from typing import Dict, Any
from app.core.config import settings


class SystemMetricsService:
    """Service for gathering system health metrics."""
    
    @staticmethod
    def get_cpu_temperature() -> Dict[str, Any]:
        """Get CPU temperature using vcgencmd (Raspberry Pi specific)."""
        try:
            result = subprocess.run(
                ["vcgencmd", "measure_temp"],
                capture_output=True,
                text=True,
                timeout=settings.health_check_timeout
            )
            if result.returncode == 0:
                temp_str = result.stdout.strip()
                # Extract temperature value (e.g., "temp=47.3'C")
                temp_value = temp_str.split("=")[1].replace("'C", "")
                return {
                    "raw": temp_str,
                    "celsius": float(temp_value),
                    "available": True
                }
        except (subprocess.TimeoutExpired, FileNotFoundError, IndexError, ValueError):
            pass
        
        # Fallback for non-Raspberry Pi systems
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try to get CPU temperature from psutil
                for name, entries in temps.items():
                    if 'cpu' in name.lower() or 'core' in name.lower():
                        if entries:
                            return {
                                "raw": f"{entries[0].current}°C",
                                "celsius": entries[0].current,
                                "available": True
                            }
        except Exception:
            pass
        
        return {"raw": "N/A", "celsius": None, "available": False}
    
    @staticmethod
    def get_throttle_status() -> Dict[str, Any]:
        """Get voltage throttling status using vcgencmd (Raspberry Pi specific)."""
        try:
            result = subprocess.run(
                ["vcgencmd", "get_throttled"],
                capture_output=True,
                text=True,
                timeout=settings.health_check_timeout
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                # Parse throttled value (hex format)
                if "=" in output:
                    hex_value = output.split("=")[1]
                    try:
                        throttled_int = int(hex_value, 16)
                        # Decode throttled flags
                        flags = {
                            "under_voltage": bool(throttled_int & 0x1),
                            "frequency_capped": bool(throttled_int & 0x2),
                            "throttled": bool(throttled_int & 0x4),
                            "soft_temp_limit": bool(throttled_int & 0x8),
                            "under_voltage_occurred": bool(throttled_int & 0x10000),
                            "frequency_capped_occurred": bool(throttled_int & 0x20000),
                            "throttled_occurred": bool(throttled_int & 0x40000),
                            "soft_temp_limit_occurred": bool(throttled_int & 0x80000),
                        }
                        return {
                            "raw": output,
                            "hex_value": hex_value,
                            "flags": flags,
                            "status": "OK" if throttled_int == 0 else "WARNING",
                            "available": True
                        }
                    except ValueError:
                        pass
                return {"raw": output, "available": True}
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return {"raw": "N/A", "available": False, "status": "N/A"}
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get CPU information including usage and frequency."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                "usage_percent": cpu_percent,
                "count": cpu_count,
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "frequency_min_mhz": cpu_freq.min if cpu_freq else None,
                "frequency_max_mhz": cpu_freq.max if cpu_freq else None,
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get RAM usage information."""
        try:
            mem = psutil.virtual_memory()
            return {
                "total_bytes": mem.total,
                "available_bytes": mem.available,
                "used_bytes": mem.used,
                "percent": mem.percent,
                "total_mb": round(mem.total / (1024 * 1024), 2),
                "available_mb": round(mem.available / (1024 * 1024), 2),
                "used_mb": round(mem.used / (1024 * 1024), 2),
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_network_stats() -> Dict[str, Any]:
        """Get network I/O statistics."""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout,
                "mbps_sent": round(net_io.bytes_sent / (1024 * 1024), 2),
                "mbps_recv": round(net_io.bytes_recv / (1024 * 1024), 2),
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_disk_info() -> Dict[str, Any]:
        """Get disk usage and I/O statistics."""
        try:
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            result = {
                "root": {
                    "total_bytes": disk_usage.total,
                    "used_bytes": disk_usage.used,
                    "free_bytes": disk_usage.free,
                    "percent": disk_usage.percent,
                    "total_gb": round(disk_usage.total / (1024 ** 3), 2),
                    "used_gb": round(disk_usage.used / (1024 ** 3), 2),
                    "free_gb": round(disk_usage.free / (1024 ** 3), 2),
                }
            }
            
            if disk_io:
                result["io"] = {
                    "read_bytes": disk_io.read_bytes,
                    "write_bytes": disk_io.write_bytes,
                    "read_count": disk_io.read_count,
                    "write_count": disk_io.write_count,
                }
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system platform information."""
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
        }
    
    @classmethod
    def get_all_metrics(cls) -> Dict[str, Any]:
        """Get all system metrics in a single call."""
        return {
            "system": cls.get_system_info(),
            "cpu": cls.get_cpu_info(),
            "memory": cls.get_memory_info(),
            "temperature": cls.get_cpu_temperature(),
            "voltage": cls.get_throttle_status(),
            "network": cls.get_network_stats(),
            "disk": cls.get_disk_info(),
        }


