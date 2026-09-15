import os
import sys

# Ensure backend root is always in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database.session import init_db, SessionLocal
from app.database.seed_data import seed_database
from app.api.auth import router as auth_router
from app.api.incidents import router as incidents_router
from app.api.analysis import router as analysis_router
from app.api.dashboard import router as dashboard_router
from app.api.risk_map import router as risk_map_router
from app.api.assets import router as assets_router
from app.api.corrective_actions import router as corrective_actions_router
from app.api.rag import router as rag_router
from app.api.alerts import router as alerts_router
from app.api.reports import router as reports_router
from app.api.copilot import router as copilot_router
from app.api.analytics import router as analytics_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-Ready Refinery and Oil & Gas Safety Incident Analysis Platform",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(analysis_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(risk_map_router, prefix=settings.API_V1_STR)
app.include_router(assets_router, prefix=settings.API_V1_STR)
app.include_router(corrective_actions_router, prefix=settings.API_V1_STR)
app.include_router(rag_router, prefix=settings.API_V1_STR)
app.include_router(alerts_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(copilot_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "OPERATIONAL",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Mount Static Files (Frontend UI) if available
static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/{full_path:path}")
def serve_frontend_spa(full_path: str):
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        asset_file = os.path.join(static_path, full_path)
        if full_path and os.path.exists(asset_file) and not os.path.isdir(asset_file):
            return FileResponse(asset_file)
        return FileResponse(index_file)
    return {
        "message": "OIL-SAFE AI API is running. Access /api/health or /docs for API documentation.",
        "incident_demo": "/api/incidents/1/analyze"
    }

if __name__ == "__main__":
    import uvicorn
    init_db()
    db = SessionLocal()
    seed_database(db)
    db.close()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
