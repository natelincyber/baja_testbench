"""
FastAPI application factory and main entry point.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
from pathlib import Path
from baja_testbench.core.config import settings
from baja_testbench.api.v1.router import api_router
from baja_testbench.services.system_metrics import SystemMetricsService


def create_application() -> FastAPI:
    """
    Application factory pattern for FastAPI.
    Allows for easier testing and configuration.
    """
    app = FastAPI(
        title=settings.app_name,
        description="Hardware-in-the-Loop test server for drivetrain subsystem validation",
        version=settings.app_version,
        debug=settings.debug,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Include API routers
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    # Serve frontend
    @app.get("/")
    async def serve_frontend():
        static_file = static_dir / "index.html"
        if static_file.exists():
            return FileResponse(str(static_file))
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "endpoints": {
                f"{settings.api_v1_prefix}/health": "System health diagnostics",
                "/docs": "API documentation (Swagger UI)",
                "/redoc": "Alternative API documentation"
            }
        }
    
    @app.websocket("/ws/system-stream")
    async def websocket_health_stream(websocket: WebSocket):
        """WebSocket endpoint for streaming system health data."""
        await websocket.accept()
        metrics_service = SystemMetricsService()
        
        try:
            while True:
                # Get current health metrics
                metrics = metrics_service.get_all_metrics()
                
                await websocket.send_json(metrics)
                
                # Wait 2 seconds before next update
                await asyncio.sleep(2)
        except WebSocketDisconnect:
            print("WebSocket client disconnected")
        except Exception as e:
            print(f"WebSocket error: {e}")
            await websocket.close()
    
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


