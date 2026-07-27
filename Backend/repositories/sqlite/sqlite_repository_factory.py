import sqlite3

from repositories.interfaces.repository_factory import RepositoryFactory
from repositories.interfaces.application_repository import ApplicationRepository
from repositories.interfaces.phase_repository import PhaseRepository
from repositories.interfaces.status_repository import StatusRepository
from repositories.sqlite.application_repository import SqliteApplicationRepository
from repositories.sqlite.status_repository import SqliteStatusRepository
from repositories.sqlite.phase_repository import SqlitePhaseRepository


# SQLite's concrete fulfilment of the RepositoryFactory contract. Built by
# get_sqlite_repository_factory() (database_connection.py) around a single
# sqlite3 connection, and hands that same connection to every repository it
# creates so they all operate within the same request-scoped connection.
class SqliteRepositoryFactory(RepositoryFactory):
    def __init__(self, conn):
        self.conn: sqlite3.Connection = conn

    def application_repository(self) -> ApplicationRepository:
        return SqliteApplicationRepository(self.conn)

    def status_repository(self) -> StatusRepository:
        return SqliteStatusRepository(self.conn)

    def phase_repository(self) -> PhaseRepository:
        return SqlitePhaseRepository(self.conn)
