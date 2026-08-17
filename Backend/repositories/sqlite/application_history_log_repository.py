import sqlite3
import datetime
from models.application_history_log import (
    BaseApplicationHistoryLog,
    ReadApplicationHistoryLog,
)
from repositories.interfaces.application_history_log_repository import (
    ApplicationHistoryLogRepository,
)


class SqliteApplicationHistoryLogRepository(ApplicationHistoryLogRepository):
    """sqlite3-backed implementation for the history logging. Everything sqlite-specific (the
    connection, the '?' placeholders, sqlite3.Row) lives only in here."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[ReadApplicationHistoryLog]:
        sql = """ SELECT * FROM application_history_log """
        cursor = self._conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()

        return [self._m_map_row_to_application_history_log(row) for row in rows]

    def get_by_id(self, id: int) -> ReadApplicationHistoryLog | None:
        sql = """ SELECT 
                    application_history_log.id as id,
                    application_history_log.application_id as application_id,
                    application_history_log.phase_id as phase_id,
                    application_history_log.status_id as status_id,
                    application_history_log.occurred_at as occurred_at
                  FROM application_history_log  
                  WHERE application_history_log.id = ?   
          """

        cursor = self._conn.cursor()
        cursor.execute(sql, (id,))

        row = cursor.fetchone()

        if not row:
            return None

        return self._map_row_to_application_history_log(row)

    def add(
        self, new_history_log: BaseApplicationHistoryLog
    ) -> ReadApplicationHistoryLog:
        sql = """ INSERT INTO application_history_log(application_id,phase_id,status_id,occurred_at) VALUES(?,?,?,?) """

        cursor = self._conn.cursor()
        cursor.execute(
            sql,
            (
                new_history_log.application_id,
                new_history_log.phase_id,
                new_history_log.status_id,
                datetime.datetime.now().date(),
            ),
        )

        self._conn.commit()

        new_id = cursor.lastrowid

        history_entry = self.get_by_id(new_id)

        return history_entry

    @staticmethod
    def _map_row_to_application_history_log(
        row: sqlite3.Row,
    ) -> ReadApplicationHistoryLog:

        application_history_log = {
            "id": row["id"],
            "application_id": row["application_id"],
            "phase_id": row["phase_id"],
            "status_id": row["status_id"],
            "occurred_at": row["occurred_at"],
        }

        return ReadApplicationHistoryLog.model_validate(application_history_log)
