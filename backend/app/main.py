"""
CrediLens — Main FastAPI Application
AI-Powered Misinformation and Fake News Credibility Analyzer
"""
from fastapi import FastAPI

app = FastAPI()

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.app.core.config import settings
from backend.app.core.errors import AppException, create_error_response
from backend.app.database.mongodb import db_manager
from backend.app.ml.loader import model_manager

# API Routers
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.system import router as system_router
from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.analyze import router as analyze_router
from backend.app.api.routes.analysis import router as analysis_router
from backend.app.api.routes.sources import router as sources_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application Startup
    print("[Lifespan] Initializing CrediLens backend services...")
    # Load ML artifacts once into memory
    model_manager.load_models()
    # Initialize async database connection (or fallback)
    await db_manager.connect()
    print("[Lifespan] CrediLens backend initialized and ready.")
    
    yield
    
    # Application Shutdown
    print("[Lifespan] Shutting down CrediLens services...")
    await db_manager.disconnect()

app = FastAPI(
    title=f"{settings.APP_NAME} API",
    description="Credibility Assessment Engine for Misinformation and Fake News Analysis",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS Configuration
origins = settings.cors_origins
if not origins or "*" in origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if "*" not in origins else ["*"],
    allow_credentials=True if "*" not in origins else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers ensuring standard envelope responses
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return create_error_response(code=exc.code, message=exc.message, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_error = errors[0] if errors else {}
    msg = first_error.get("msg", "Invalid request parameters.")
    loc = " -> ".join([str(x) for x in first_error.get("loc", [])])
    detail_msg = f"{loc}: {msg}" if loc else msg
    return create_error_response(code="INVALID_INPUT", message=detail_msg, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code = "NOT_FOUND" if exc.status_code == 404 else ("UNAUTHORIZED" if exc.status_code == 401 else "INTERNAL")
    return create_error_response(code=code, message=str(exc.detail), status_code=exc.status_code)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"[Unhandled Error] {type(exc).__name__}: {str(exc)}")
    return create_error_response(code="INTERNAL", message="An unexpected server error occurred.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Register Routers
app.include_router(health_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(sources_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "academicTitle": "AI-Powered Misinformation and Fake News Credibility Analyzer",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
