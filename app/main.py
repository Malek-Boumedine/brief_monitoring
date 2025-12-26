from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import engine
from app.routes import items_router
from app.monitoring.metrics import app_info


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Gestion du cycle de vie de l'application."""
    # Startup
    SQLModel.metadata.create_all(engine)
    
    # Configurer les informations de l'application
    app_info.info({
        'version': '1.0.0',
        'environment': 'development'
    })
    
    yield
    # Shutdown (si nécessaire)


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles avec monitoring Prometheus",
    version="1.0.0",
    lifespan=lifespan,
)

# Instrumentation automatique Prometheus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
)

instrumentator.instrument(app).expose(app, endpoint="/metrics")

# Routes
app.include_router(items_router)


@app.get("/")
def root():
    return {"message": "Items CRUD API with Prometheus monitoring"}


@app.get("/health")
def health():
    return {"status": "healthy"}
