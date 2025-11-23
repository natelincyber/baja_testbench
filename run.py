#!/usr/bin/env python3
"""
Application entry point for running the FastAPI server.
"""

import uvicorn
from baja_testbench.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "baja_testbench.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


