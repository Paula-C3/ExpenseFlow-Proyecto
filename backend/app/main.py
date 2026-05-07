from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.database import init_db, SessionLocal
from app.api.routes import auth
from app.api.routes import requests_router
from app.api.routes import notifications_router
from app.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from app.infrastructure.event_bus.listeners import NotificationListener, AuditListener
from app.infrastructure.orm.notification_repository import NotificationRepository
from app.infrastructure.orm.audit_log_repository import AuditLogRepository
from app.domain.factories.singleton import EventBusRegistry
from app.domain.events import (
    RequestApprovedEvent,
    RequestCreatedEvent,
    RequestRejectedEvent,
    RequestSubmittedEvent,
    RequestStatusChangedEvent,
)

app = FastAPI(
    title="ExpenseFlow API",
    description="Sistema de gestión de gastos y reembolsos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(requests_router.router)
app.include_router(notifications_router.router)


@app.on_event("startup")
async def startup():
    init_db()

    db = SessionLocal()

    event_bus = MemoryEventBus()

    notification_listener = NotificationListener(
        NotificationRepository(db)
    )

    audit_listener = AuditListener(
        AuditLogRepository(db)
    )

    event_bus.subscribe(RequestCreatedEvent, notification_listener)
    event_bus.subscribe(RequestSubmittedEvent, notification_listener)
    event_bus.subscribe(RequestApprovedEvent, notification_listener)
    event_bus.subscribe(RequestRejectedEvent, notification_listener)

    event_bus.subscribe(RequestStatusChangedEvent, audit_listener)
    event_bus.subscribe(RequestApprovedEvent, audit_listener)
    event_bus.subscribe(RequestRejectedEvent, audit_listener)

    EventBusRegistry().set_event_bus(event_bus)


@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a ExpenseFlow API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
