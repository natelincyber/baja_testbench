"""
FastAPI application factory and main entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router


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
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Include API routers
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "endpoints": {
                f"{settings.api_v1_prefix}/health": "System health diagnostics",
                "/docs": "API documentation (Swagger UI)",
                "/redoc": "Alternative API documentation"
            }
        }
    
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


