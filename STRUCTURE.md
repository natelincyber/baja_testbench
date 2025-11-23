# Project Structure

This document describes the production-ready FastAPI application structure for the Baja Testbench HIL system.

## Directory Structure

```
BajaTestbench/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app factory and entry point
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependency injection
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── health.py         # Health check endpoints
│   │       └── router.py         # Router aggregation
│   ├── core/                     # Core application logic
│   │   ├── __init__.py
│   │   └── config.py             # Settings and configuration
│   ├── models/                   # Pydantic models
│   │   ├── __init__.py
│   │   └── health.py             # Health check models
│   └── services/                 # Business logic services
│       ├── __init__.py
│       └── system_metrics.py     # System metrics collection
│
├── modules/                      # Modular components (monorepo style)
│   ├── __init__.py
│   └── health_check/             # Health check module
│       ├── __init__.py
│       ├── models.py             # Module-specific models
│       └── service.py            # Module-specific services
│
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

## Architecture Overview

### Application Layer (`app/`)

- **`main.py`**: FastAPI application factory using the factory pattern for easier testing and configuration
- **`api/`**: REST API endpoints organized by version
  - Uses dependency injection for services
  - Versioned API routes (`/api/v1/`)
- **`core/`**: Core application configuration
  - Settings management with Pydantic Settings
  - Environment variable support
- **`models/`**: Pydantic models for request/response validation
- **`services/`**: Business logic separated from API layer
  - System metrics collection
  - Reusable service classes

### Module Layer (`modules/`)

Each module represents a distinct aspect of the project and can be developed independently:

- **`health_check/`**: Health monitoring module
  - Can be extended with module-specific functionality
  - Wraps core services for module-specific use cases

## Key Features

1. **Production-Ready Structure**: Follows FastAPI best practices
2. **Separation of Concerns**: Clear separation between API, services, and models
3. **Dependency Injection**: Services injected via FastAPI dependencies
4. **Type Safety**: Pydantic models for validation and type checking
5. **Configuration Management**: Environment-based configuration
6. **Modular Design**: Monorepo-style modules for independent development
7. **Versioned API**: API routes organized by version for future compatibility

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /api/v1/health` - System health diagnostics
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Adding New Modules

To add a new module:

1. Create a new directory under `modules/`
2. Add module-specific code (services, models, etc.)
3. Import and use in the main application as needed

Example:
```
modules/
├── actuator_control/
│   ├── __init__.py
│   ├── service.py
│   └── models.py
├── telemetry/
│   ├── __init__.py
│   ├── service.py
│   └── models.py
```


