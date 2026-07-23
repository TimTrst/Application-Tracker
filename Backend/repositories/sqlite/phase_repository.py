import sqlite3
from models.phase import ReadPhase, BasePhaseOptional, BasePhase
from repositories.interfaces.phase_repository import PhaseRepository

BASE_PHASE_QUERY = """
                SELECT
                    phase.id as phase_id,
                    phase.name as phase_name
                FROM phase
                """


class SqlitePhaseRepository(PhaseRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[ReadPhase]:
        cursor = self._conn.cursor()
        cursor.execute(BASE_PHASE_QUERY)

        rows = cursor.fetchall()

        return [self._map_row_to_phase(row) for row in rows]

    def get_by_id(self, id: int) -> ReadPhase | None:
        cursor = self._conn.cursor()
        cursor.execute(BASE_PHASE_QUERY + """WHERE phase.id = ?""", (id,))

        row = cursor.fetchone()

        if not row:
            return None

        return self._map_row_to_phase(row)

    def add(self, new_phase: BasePhase) -> ReadPhase | None:
        sql = """ INSERT INTO phase(name)
                VALUES(?) """

        cursor = self._conn.cursor()
        cursor.execute(sql, (new_phase.name,))

        self._conn.commit()

        new_id = cursor.lastrowid

        return self.get_by_id(new_id, self._conn)

    def remove(self, id: int) -> bool:
        sql = """DELETE FROM phase WHERE id = ?"""

        cursor = self._conn.cursor()
        cursor.execute(sql, (id,))
        self._conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    def modify(
        self, id: int, updated_phase: BasePhaseOptional
    ) -> ReadPhase | None | bool:
        data_to_update = updated_phase.model_dump(exclude_unset=True)

        if not data_to_update:
            return False

        sql = """UPDATE phase SET name = ? WHERE id = ?"""

        cursor = self._conn.cursor()

        cursor.execute(sql, (data_to_update["name"], id))

        self._conn.commit()

        result = self.get_by_id(id, self._conn)
        print(f"Result after update: {result}")
        return result

    @staticmethod
    def _map_row_to_phase(row) -> ReadPhase:
        phase = {
            "id": row["phase_id"],
            "name": row["phase_name"],
        }

        return ReadPhase.model_validate(phase)
