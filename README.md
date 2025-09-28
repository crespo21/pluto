# Pluto API Blueprint

This repository is a teaching scaffold that walks a Python beginner through the way a production-ready API is usually organised. It emphasises clean layering, explicit boundaries, and the workflows you will repeat every day: adding endpoints, evolving the data model with migrations, and keeping the code easy to test.

---

## Quick start

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configure the database engine** – by default we use SQLite (`sqlite:///./pluto.db`). For another engine, change the URL in `src/infrastructure/database/config.py` or read it from an environment variable.
3. **Generate the schema** – once migrations are in place (see below), run `alembic upgrade head`. For the first run you can call the helper in `config.py` to create tables directly while you bootstrap.
4. **Smoke test the stack** – run the unit test suite or manually invoke the service layer from a Python shell to confirm reads and writes work end-to-end.

> 📝 Keep the virtual environment activated while you work; it ensures consistent dependencies across the team.

---

## Layered architecture tour

```
src/
├── domain/         # Pure business rules (entities, enums, repository contracts)
├── application/    # DTOs and use-case services
├── infrastructure/ # ORMs, sessions, migrations, concrete repositories
└── presentation/   # HTTP-facing controllers (FastAPI/Flask blueprint to be filled in)
```

Each layer only speaks to the one directly beneath it:

- `domain` knows nothing about persistence or HTTP. The `User` entity and `UserRepository` contract live here.
- `application` coordinates use cases. `UserService` converts DTOs to domain entities, hands them to the repository, and maps results back.
- `infrastructure` fulfils the `UserRepository` contract using SQLAlchemy models and sessions.
- `presentation` will host the web framework (e.g., FastAPI). Controllers should depend on services, never on infrastructure types directly.

This separation lets you test business rules without the database, swap persistence tech, or expose the same use cases via HTTP, CLI, or background jobs.

---

## Data model & migrations

### ORM model

- `src/infrastructure/database/models/user_model.py` defines the `UserModel` SQLAlchemy table.
- `UserModel.to_domain()` and `.from_domain()` convert between the persistence shape and the pure `domain.entities.user.User`.

### Session & engine

`src/infrastructure/database/config.py` owns the SQLAlchemy engine and session factory. In production you should:

- Read the `DATABASE_URL` environment variable and call `create_engine(DATABASE_URL, future=True)`.
- Provide a `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)` factory instead of a global session. Dependency-inject sessions per request to avoid cross-request leakage.

### Alembic workflow

1. **Initialise**: `alembic init src/infrastructure/migrations` (already present in this repo – confirm `alembic.ini` is configured to use `UserModel.metadata`).
2. **Autogenerate**: after editing models, run `alembic revision --autogenerate -m "describe change"`.
3. **Review**: open the generated script, tweak constraints and downgrade logic.
4. **Apply**: `alembic upgrade head`. For local resets use `alembic downgrade base` followed by another upgrade.

Tips:

- Always run migrations inside a transaction (Alembic does this by default for supported backends).
- Keep seed scripts separate from schema migrations.
- Tag releases by the Alembic revision you deployed; it speeds up rollback decisions.

---

## Implementing an API endpoint

1. **Define/extend DTOs** – update `UserDTO` or add new dataclasses for request/response payloads.
2. **Add service logic** – place orchestration code in `UserService` (create new services for other aggregates). Services should only call repository interfaces.
3. **Wire the repository** – `SqlAlchemyUserRepository` implements the domain contract using SQLAlchemy. Ensure helper functions (`_persist`, `_ensure_status`, etc.) remain at the class scope, not nested inside `__init__`.
4. **Expose via presentation layer** – choose a framework (FastAPI recommended for async support). In `presentation/api/user_controller.py`, create routers that depend on the service. Example skeleton:

   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from src.application.dto.user_dto import UserDTO
   from src.application.services.user_services import UserService

   router = APIRouter(prefix="/users", tags=["users"])

   @router.post("", response_model=UserDTO)
   def create_user(payload: UserDTO, service: UserService = Depends(get_user_service)):
	   try:
		   return service.create_user(payload)
	   except UserAlreadyExistsError as exc:
		   raise HTTPException(status_code=409, detail=str(exc))
   ```

5. **Document** – describe request/response shapes using Pydantic models or JSON schemas so API consumers know what to expect.
6. **Test** – unit test the service (pure Python) and integration test the router using the framework’s test client with a transactional, throwaway database.

---

## Testing strategy

- **Unit tests**: target `domain` and `application` layers. Use fakes for `UserRepository` when testing services.
- **Integration tests**: spin up a temporary database, run migrations, and hit the `SqlAlchemyUserRepository` directly.
- **End-to-end tests**: exercise HTTP endpoints using the chosen framework’s test client (e.g., FastAPI’s `TestClient`).

Structure tests in a mirrored directory tree (`tests/domain`, `tests/application`, etc.) and run them with `pytest`.

---

## Production-readiness checklist

- ✅ Configuration via environment variables (no secrets committed).
- ✅ Database migrations tracked by Alembic.
- ✅ Layered architecture enabling dependency inversion.
- ✅ DTOs enforce contract between layers.
- ✅ Structured logging (`logging` module) inside repositories and services.
- ✅ Observability hooks (add OpenTelemetry exporters when ready).
- ✅ CI pipeline that runs linting (`ruff`/`flake8`) and tests.
- ✅ Containerisation (add a Dockerfile using multi-stage builds once the API is live).

Treat this checklist as your definition of done for every feature.

---

## Known gaps & next steps

- `SqlAlchemyUserRepository` currently defines helper methods inside `__init__`, which means they are not registered as real methods. Unindent those helpers so they become class-level methods.
- Introduce dependency-injection utilities to provide per-request sessions and services when the presentation layer is implemented.
- Fill `presentation/api/user_controller.py` with a concrete web framework implementation.
- Add a `tests/` package with coverage for services and repositories.
- Replace the ad-hoc session in `config.py` with a `sessionmaker` factory and context manager helpers.

Once these are addressed, you will have a solid, production-ready foundation that scales with new features and teammates.

