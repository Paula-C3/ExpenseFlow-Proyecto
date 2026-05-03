# 💸 ExpenseFlow

Plataforma de aprobación de gastos y reembolsos.

---

## Caso de negocio

**ExpenseFlow** resuelve el problema de gestión manual de gastos corporativos. Actualmente los empleados envían solicitudes por correo, lo que genera pérdida de información, gastos duplicados y falta de trazabilidad sobre quién aprobó qué y cuándo.

El MVP centraliza el flujo: creación de solicitud → aprobación por rol → notificación → auditoría → marcado como pagado.

Reglas de aprobación por monto:
| Monto | Flujo de aprobación |
|-------|---------------------|
| ≤ $50 USD | No requiere aprobación de manager, va directo a Revisión de Finanzas |
| $50-$500 USD | Requiere aprobación de Manager |
| > $500 USD | Requiere aprobación de Manager + Finance Admin |

---

## Integrantes

| Persona | Área |
|---------|------|
| Persona 1 | Discovery — Contexto y Requerimientos |
| Persona 2 | Discovery — Flujos, Eventos y Alcance |
| Persona 3 | UML |
| Persona 4 | GitHub Project e Issues |
| Persona 5 | DevOps — Repo, CI/CD, Docker, Render |

---

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI + Python 3.11 |
| Validación de datos | Pydantic v2 |
| Autenticación | JWT (python-jose + PyJWT) + bcrypt |
| Frontend | Streamlit (en desarrollo) |
| Base de datos | PostgreSQL 16 (producción), SQLite (tests) |
| ORM | SQLAlchemy 2 |
| Infraestructura | Docker + Docker Compose |
| CI/CD | GitHub Actions + Docker Hub + Render |
| Lint | Ruff |
| Tests | Pytest + pytest-asyncio + httpx |
| Patrones de diseño | Factory, Singleton, State, Strategy, Command, Template Method, Observer |

---

## Arquitectura

El proyecto sigue **arquitectura hexagonal** con separación estricta de capas:

```
backend/app/
├── domain/          # Entidades, value objects, enums, reglas de negocio, interfaces
├── application/     # Casos de uso, DTOs, servicios de aplicación
├── infrastructure/  # ORM (SQLAlchemy), repositorios concretos, event bus, DB
└── api/             # Rutas FastAPI, dependencias, controladores
```

El dominio **no depende** de FastAPI, SQLAlchemy ni Streamlit.

Se implementan 7 patrones de diseño: Factory, Singleton, State, Strategy, Command, Template Method y Observer (Event Bus) para gestionar la lógica de negocio y eventos de dominio.

---

## API Endpoints

La API de FastAPI expone los siguientes endpoints (documentación interactiva disponible en `http://localhost:8000/docs`):

### Autenticación (`/auth`)
| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| POST | `/auth/login` | Inicio de sesión con email/contraseña | Público |
| POST | `/auth/register` | Registro de nuevos usuarios (rol por defecto: EMPLOYEE) | Público |
| GET | `/auth/me` | Obtener información del usuario actual (JWT) | Autenticado |
| GET | `/auth/users` | Listar todos los usuarios | SYSTEM_ADMIN |

### Solicitudes de Gasto (`/requests`)
| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| POST | `/requests` | Crear nueva solicitud de gasto | EMPLOYEE |
| GET | `/requests` | Listar solicitudes (filtradas por rol) | Todos los roles |
| GET | `/requests/{request_id}` | Obtener detalle de solicitud | Todos los roles |
| POST | `/requests/{request_id}/approve` | Aprobar solicitud | MANAGER, FINANCE_ADMIN, SYSTEM_ADMIN |
| POST | `/requests/{request_id}/reject` | Rechazar solicitud | MANAGER, FINANCE_ADMIN, SYSTEM_ADMIN |

### Notificaciones y Auditoría (`/notifications`, `/audit`)
| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| GET | `/notifications` | Obtener notificaciones del usuario | Autenticado |
| PATCH | `/notifications/{id}/read` | Marcar notificación como leída | Autenticado |
| GET | `/audit` | Obtener logs de auditoría (filtrado por request_id) | SYSTEM_ADMIN |

---

## Modelos de Base de Datos

El proyecto usa SQLAlchemy 2 como ORM, con las siguientes tablas principales:

| Tabla | Descripción |
|-------|-------------|
| `users` | Usuarios del sistema, con campos: id, email, full_name, hashed_password, role_id, is_active |
| `roles` | Roles de usuario (EMPLOYEE, MANAGER, FINANCE_ANALYST, FINANCE_ADMIN, SYSTEM_ADMIN) |
| `requests` | Solicitudes de gasto, con campos: id, employee_id, title, amount, category, status, receipt_url |
| `approvals` | Registro de aprobaciones de solicitudes, con campos: request_id, approver_id, approval_type, comment |
| `audit_logs` | Logs de auditoría de todas las acciones, con campos: actor_id, entity_type, action, previous_state, new_state |
| `notifications` | Notificaciones in-app para usuarios, con campos: user_id, title, message, is_read, request_id |

Relaciones principales:
- Un rol tiene muchos usuarios; un usuario pertenece a un rol.
- Un usuario (empleado) tiene muchas solicitudes de gasto.
- Una solicitud tiene muchas aprobaciones, notificaciones y logs de auditoría.

---

## Patrones de Diseño

El proyecto implementa 7 patrones de diseño para gestionar la lógica de negocio y eventos:

| Patrón | Propósito |
|--------|-----------|
| Factory | Crear objetos `Request` con validaciones de value objects |
| Singleton | Gestionar configuraciones globales y el Event Bus compartido |
| State | Gestionar transiciones de estado de las solicitudes (SUBMITTED → APPROVED → PAID, etc.) |
| Strategy | Seleccionar lógica de aprobación según el monto de la solicitud |
| Command | Encapsular comandos de aprobación/rechazo de solicitudes |
| Template Method | Definir el flujo base de procesamiento de solicitudes con hooks para validación y notificación |
| Observer (Event Bus) | Publicar eventos de dominio (creación, aprobación, rechazo) para generar auditoría y notificaciones automáticas |

---

## Pruebas

El proyecto usa Pytest con pytest-asyncio y httpx para pruebas de la API. Para ejecutar las pruebas:

```bash
cd backend
pytest                           # Ejecutar todas las pruebas
pytest -v                         # Salida detallada
pytest backend/app/tests/test_create_request.py  # Ejecutar prueba específica
```

Pruebas implementadas (16 archivos en `backend/app/tests/`):
- `test_create_request.py`: Casos de uso de creación de solicitudes
- `test_approve_request.py`: Casos de uso de aprobación de solicitudes
- `test_auth.py`: Endpoints de autenticación
- `test_builder.py`: Builder de AuditLog
- `test_command.py`: Patrón Command
- `test_event_bus.py`: Event Bus y listeners
- `test_factory.py`: Factory de Request
- `test_state.py`: Patrón State
- `test_strategy.py`: Patrón Strategy
- `test_template_method.py`: Patrón Template Method
- `test_value_objects.py`: Value objects (Email, Money, RequestTitle)
- Entre otros.

---

## Cómo correr localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/<usuario>/ExpenseFlow-Proyecto.git
cd ExpenseFlow-Proyecto
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env si es necesario
```

### 3. Instalar dependencias del backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Correr el backend

```bash
uvicorn app.main:app --reload
# Disponible en http://localhost:8000
```

### 5. Correr el frontend (otra terminal)
> ⚠️ El frontend está en etapa de desarrollo; el archivo `requirements.txt` del frontend aún no está creado, las dependencias de Streamlit se encuentran en el `requirements.txt` raíz.
```bash
cd frontend
pip install -r ../requirements.txt  # Instala Streamlit y dependencias
streamlit run app/main.py
# Disponible en http://localhost:8501
```

---

## Cómo correr con Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

| Servicio | URL |
|----------|-----|
| Backend (API) | http://localhost:8000 |
| Frontend | http://localhost:8501 |
| PostgreSQL | localhost:5432 |

Para detener:
```bash
docker compose down
```

Para limpiar volúmenes (base de datos):
```bash
docker compose down -v
```

---

## Flujo GitHub Actions

El pipeline tiene tres etapas según el evento:

### PR hacia `dev` → CI
- Instala dependencias
- Corre lint (ruff)
- Corre tests (pytest)

### Push/merge a `dev` → CI + Deploy dev
- Todo lo anterior
- Build y push de imagen con tag `:dev` a Docker Hub
- Dispara redeploy en Render (ambiente dev)

### Push de tag `v*` a `main` → Deploy producción
- Validaciones completas (lint + tests)
- Build y push de imagen con tag `:prod` a Docker Hub
- Dispara redeploy en Render (ambiente prod)

> ⚠️ No se acepta deploy directo a producción desde ramas feature.
> ⚠️ Los archivos de workflow de GitHub Actions (`ci-cd.yml`, `deploy.yml`) están actualmente vacíos y pendientes de configuración.

---

## Ambientes en Render

| Ambiente | Imagen Docker Hub | URL |
|----------|------------------|-----|
| dev | `<usuario>/expenseflow-backend:dev` | _(pendiente)_ |
| prod | `<usuario>/expenseflow-backend:prod` | _(pendiente)_ |

---

## Secrets requeridos en GitHub

Configurar en **Settings → Secrets and variables → Actions**:

| Secret | Descripción |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Usuario de Docker Hub |
| `DOCKERHUB_TOKEN` | Token de acceso de Docker Hub |
| `RENDER_DEV_DEPLOY_HOOK` | Deploy hook del servicio dev en Render |
| `RENDER_PROD_DEPLOY_HOOK` | Deploy hook del servicio prod en Render |
