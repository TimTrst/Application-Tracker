# FastAPI dependency wiring: this is the single place that connects the
# abstract repository interfaces (used by routes) to a concrete database
# backend. Routes only ever depend on the `get_*_repository` functions
# below and the interface types - never on a specific DB implementation.
# To add a new backend (e.g. PostgreSQL), implement RepositoryFactory for
# it and register it in `_providers`; nothing outside this file changes.
from fastapi import Depends
import os

# Interfaces
from repositories.interfaces.repository_factory import RepositoryFactory
from repositories.interfaces.application_repository import ApplicationRepository
from repositories.interfaces.status_repository import StatusRepository
from repositories.interfaces.phase_repository import PhaseRepository

# Factory of concrete DB implementaiton
from repositories.sqlite.database_connection import get_sqlite_repository_factory

# Maps a backend name to the FastAPI dependency that builds its
# RepositoryFactory. The active backend is chosen once at import time via
# the DATABASE_BACKEND env var (defaults to sqlite).
_providers = {"sqlite": get_sqlite_repository_factory}
_active_provider = _providers[os.getenv("DATABASE_BACKEND", "sqlite")]


def get_repository_factory(
    factory: RepositoryFactory = Depends(_active_provider),
) -> RepositoryFactory:
    # Thin passthrough so downstream dependencies depend on the
    # RepositoryFactory interface rather than the active provider function.
    return factory


def get_application_repository(
    factory: RepositoryFactory = Depends(get_repository_factory),
) -> ApplicationRepository:
    # Injectable for routes: `repo: ApplicationRepository = Depends(get_application_repository)`.
    return factory.create_application_repository()


def get_status_repository(
    factory: RepositoryFactory = Depends(get_repository_factory),
) -> StatusRepository:
    # Injectable for routes: `repo: StatusRepository = Depends(get_status_repository)`.
    return factory.create_status_repository()


def get_phase_repository(
    factory: RepositoryFactory = Depends(get_repository_factory),
) -> PhaseRepository:
    # Injectable for routes: `repo: PhaseRepository = Depends(get_phase_repository)`.
    return factory.create_phase_repository()
