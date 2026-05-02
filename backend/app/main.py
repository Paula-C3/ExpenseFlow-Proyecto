from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.infrastructure.database import init_db
from backend.app.api.routes import auth
from backend.app.api.routes import requests_router
from backend.app.api.routes import notifications_router



app = FastAPI(
    title="ExpenseFlow API",
    description="Sistema de gestión de gastos y reembolsos",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(requests_router.router)
app.include_router(notifications_router.router)

# Event startup
@app.on_event("startup")
async def startup():
    """Inicializa la base de datos al iniciar."""
    init_db()


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Bienvenido a ExpenseFlow API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
