#!/usr/bin/env python3
import uvicorn
from baja_testbench.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "baja_testbench.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


