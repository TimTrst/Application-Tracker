import sqlite3
from fastapi import Depends
from database.database import get_db
from repositories.interfaces.application_repository import ApplicationRepository
from repositories.interfaces.status_repository import StatusRepository
from repositories.interfaces.phase_repository import PhaseRepository
from repositories.sqlite.application_repository import SqliteApplicationRepository
from repositories.sqlite.status_repository import SqliteStatusRepository
from repositories.sqlite.phase_repository import SqlitePhaseRepository


def get_application_repository(
    conn: sqlite3.Connection = Depends(get_db),
) -> ApplicationRepository:
    return SqliteApplicationRepository(conn)


def get_status_repository(
    conn: sqlite3.Connection = Depends(get_db),
) -> StatusRepository:
    return SqliteStatusRepository(conn)


def get_phase_repository(
    conn: sqlite3.Connection = Depends(get_db),
) -> PhaseRepository:
    return SqlitePhaseRepository(conn)
