import sqlite3
from models.status import ReadStatus, WriteStatus, UpdateStatus
from repositories.interfaces.status_repository import StatusRepository

BASE_STATUS_QUERY = """
                SELECT
                    status.id as status_id,
                    status.name as status_name,
                    phase.id as phase_id,
                    phase.name as phase_name
                FROM status
                    LEFT JOIN phase ON status.phase_id = phase.id
                """


class SqliteStatusRepository(StatusRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[ReadStatus]:
        cursor = self._conn.cursor()
        cursor.execute(BASE_STATUS_QUERY)

        rows = cursor.fetchall()

        return [self._map_row_to_status(row) for row in rows]

    def get_by_id(self, id: int) -> ReadStatus | None:
        cursor = self._conn.cursor()
        cursor.execute(BASE_STATUS_QUERY + """WHERE status.id = ?""", (id,))

        row = cursor.fetchone()

        if not row:
            return None

        return self._map_row_to_status(row)

    def add(self, new_status: WriteStatus) -> ReadStatus | None:
        sql = """ INSERT INTO status(name, phase_id)
                VALUES(?,?) """

        cursor = self._conn.cursor()
        cursor.execute(sql, (new_status.name, new_status.phase_id))

        self._conn.commit()

        new_id = cursor.lastrowid

        return self.get_by_id(new_id, self._conn)

    def remove(self, id: int) -> bool:
        sql = """DELETE FROM status WHERE id = ?"""

        cursor = self._conn.cursor()
        cursor.execute(sql, (id,))
        self._conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    def modify(self, id: int, updated_status: UpdateStatus) -> ReadStatus | None | bool:
        data_to_update = updated_status.model_dump(exclude_unset=True)

        if not data_to_update:
            return False

        old_status = self.get_by_id(id, self._conn)

        merged_status = {"name": old_status.name, "phase_id": old_status.phase.id}

        merged_status.update(data_to_update)

        sql = """UPDATE status SET name = ?, phase_id = ? WHERE id = ?"""

        cursor = self._conn.cursor()

        cursor.execute(sql, (merged_status["name"], merged_status["phase_id"], id))

        self._conn.commit()

        result = self.get_by_id(id, self._conn)
        print(f"Result after update: {result}")
        return result

    @staticmethod
    def _map_row_to_status(row) -> ReadStatus:
        status = {
            "id": row["status_id"],
            "name": row["status_name"],
            "phase": {
                "id": row["phase_id"],
                "name": row["phase_name"],
            },
        }

        return ReadStatus.model_validate(status)
