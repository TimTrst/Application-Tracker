import sqlite3
from models.phase import ReadPhase, BasePhaseOptional, BasePhase

BASE_PHASE_QUERY = '''
                SELECT
                    phase.id as phase_id,
                    phase.name as phase_name
                FROM phase
                '''


def _map_row_to_phase(row) -> ReadPhase:
    phase = {
        "id": row["phase_id"],
        "name": row["phase_name"],
    }

    return ReadPhase.model_validate(phase)


def get_all_phases(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(BASE_PHASE_QUERY)

    rows = cursor.fetchall()

    return [_map_row_to_phase(row) for row in rows]


def get_phase_by_id(id, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(BASE_PHASE_QUERY +
                   '''WHERE phase.id = ?''', (id, ))

    row = cursor.fetchone()

    if not row:
        return None

    return _map_row_to_phase(row)


def add_phase(new_phase: BasePhase, conn: sqlite3.Connection):
    sql = ''' INSERT INTO phase(name)
              VALUES(?) '''

    cursor = conn.cursor()
    cursor.execute(sql, (new_phase.name, ))

    conn.commit()

    new_id = cursor.lastrowid

    return get_phase_by_id(new_id, conn)


def remove_phase(id: int, conn: sqlite3.Connection):
    sql = '''DELETE FROM phase WHERE id = ?'''

    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False
    return True


def modify_phase(id: int, updated_phase: BasePhaseOptional, conn: sqlite3.Connection):
    data_to_update = updated_phase.model_dump(exclude_unset=True)

    if not data_to_update:
        return False

    print(data_to_update)

    # old_phase = get_phase_by_id(id, conn)

    # merged_phase = {
    #     "name": old_phase.name
    # }

    # merged_phase.update(data_to_update)

    sql = '''UPDATE phase SET name = ? WHERE id = ?'''

    cursor = conn.cursor()

    cursor.execute(sql, (data_to_update["name"], id))

    conn.commit()

    result = get_phase_by_id(id, conn)
    print(f"Result after update: {result}")
    return result
