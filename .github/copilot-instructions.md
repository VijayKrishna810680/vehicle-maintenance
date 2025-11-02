# Copilot Coding Agent Instructions for Vehicle Maintenance Project

## Project Overview
- **Architecture:**
  - Monorepo with `backend` (FastAPI, PostgreSQL, Alembic, Docker), `frontend` (React), `infra` (Docker Compose), `databricks` (ETL Python notebook), and `docs` (deliverables, Postman collection).
  - Backend exposes REST API and `/chat` endpoint (LangChain agent integration).
  - Frontend communicates with backend via HTTP.
  - CI/CD via Jenkinsfile; cloud deployment notes for GCP/AWS.

## Key Workflows
- **Local Development:**
  - Start all services: `Set-Location infra; docker compose up --build`
  - Backend API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Frontend: [http://localhost:3000](http://localhost:3000)
  - Frontend dev separately: `Set-Location frontend; npm install; npm start`
- **Testing:**
  - Backend tests: `Set-Location backend; pytest tests/`
- **Database Migrations:**
  - Alembic config: `backend/alembic/`
  - Create migration: `Set-Location backend; alembic revision --autogenerate -m "description"`
  - Apply migrations: `Set-Location backend; alembic upgrade head`
- **ETL/Analytics:**
  - Databricks notebook: `databricks/etl_notebook.py`

## Project Structure & Conventions
- **Backend (`backend/app/`):**
  - FastAPI app in `main.py` with CORS and dependency injection
  - CRUD operations in `crud.py`
  - SQLAlchemy models in `models.py` (Vehicle table)
  - Pydantic schemas in `schemas.py` (VehicleCreate, VehicleOut, etc.)
  - LangChain agent in `agent.py` with fallback for missing API keys
  - Database config in `database.py` with connection pooling
- **Frontend (`frontend/src/`):**
  - React SPA in `App.js` with vehicle CRUD and chat interface
  - Uses environment variable `REACT_APP_API_URL` for backend connection
  - Axios for HTTP requests, responsive form layout
- **Infrastructure (`infra/`):**
  - Docker Compose with services: `db` (PostgreSQL), `backend` (FastAPI), `frontend` (React dev server)
  - Volume mounts for development hot-reload
- **Testing:**
  - Uses SQLite in-memory database for isolated tests
  - Dependency override pattern for database sessions
  - Comprehensive test coverage for CRUD and chat endpoints

## Integration Points
- **Database:** PostgreSQL with Alembic migrations, SQLAlchemy ORM
- **LangChain Agent:** Optional OpenAI integration with graceful fallback
- **Docker:** Multi-service development environment with networking
- **Environment Variables:**
  - `DATABASE_URL` - PostgreSQL connection string
  - `OPENAI_API_KEY` - Optional for LangChain agent
  - `REACT_APP_API_URL` - Frontend to backend connection

## Development Patterns
- **Error Handling:** HTTP exceptions with detailed messages, graceful fallbacks
- **Database:** Session dependency injection, connection pooling, migration-first schema changes
- **Frontend:** React hooks, environment-based configuration, responsive design
- **Testing:** Isolated test database, dependency overrides, comprehensive coverage

## Quick Start Commands
```powershell
# Start full stack
Set-Location infra
docker compose up --build

# Run tests
Set-Location backend
pytest tests/

# Create database migration
Set-Location backend
alembic revision --autogenerate -m "add new field"
alembic upgrade head
```

---

For more details, see `README.md` and `docs/`. The system gracefully handles missing dependencies and provides useful fallbacks.
