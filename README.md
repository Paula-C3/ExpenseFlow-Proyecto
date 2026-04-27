# 💸 ExpenseFlow

Plataforma de aprobación de gastos y reembolsos.

---

## Caso de negocio

**ExpenseFlow** resuelve el problema de gestión manual de gastos corporativos. Actualmente los empleados envían solicitudes por correo, lo que genera pérdida de información, gastos duplicados y falta de trazabilidad sobre quién aprobó qué y cuándo.

El MVP centraliza el flujo: creación de solicitud → aprobación por rol → notificación → auditoría → marcado como pagado.

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
| Frontend | Streamlit |
| Base de datos | PostgreSQL 16 |
| ORM | SQLAlchemy 2 |
| Infraestructura | Docker + Docker Compose |
| CI/CD | GitHub Actions + Docker Hub + Render |
| Lint | Ruff |
| Tests | Pytest |

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

```bash
cd frontend
pip install -r requirements.txt
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
