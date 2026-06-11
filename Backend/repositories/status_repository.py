import sqlite3
from models.status import ReadStatus, WriteStatus, UpdateStatus

BASE_STATUS_QUERY = '''
                SELECT
                    status.id as status_id,
                    status.name as status_name,
                    phase.id as phase_id,
                    phase.name as phase_name
                FROM status
                    LEFT JOIN phase ON status.phase_id = phase.id
                '''


def _map_row_to_status(row) -> ReadStatus:
    status = {
        "id": row["status_id"],
        "name": row["status_name"],
        "phase": {
            "id": row["phase_id"],
            "name": row["phase_name"],
        }
    }

    return ReadStatus.model_validate(status)


def get_all_states(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(BASE_STATUS_QUERY)

    rows = cursor.fetchall()

    return [_map_row_to_status(row) for row in rows]


def get_status_by_id(id, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(BASE_STATUS_QUERY +
                   '''WHERE status.id = ?''', (id, ))

    row = cursor.fetchone()

    if not row:
        return None

    return _map_row_to_status(row)


def add_status(new_status: WriteStatus, conn: sqlite3.Connection):
    sql = ''' INSERT INTO status(name, phase_id)
              VALUES(?,?) '''

    cursor = conn.cursor()
    cursor.execute(sql,
                   (new_status.name, new_status.phase_id)
                   )

    conn.commit()

    new_id = cursor.lastrowid

    return get_status_by_id(new_id, conn)


def remove_status(id: int, conn: sqlite3.Connection):
    sql = '''DELETE FROM status WHERE id = ?'''

    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False
    return True


def modify_status(id: int, updated_status: UpdateStatus, conn: sqlite3.Connection):
    data_to_update = updated_status.model_dump(exclude_unset=True)

    if not data_to_update:
        return False

    old_status = get_status_by_id(id, conn)

    print("old", old_status)
    print("new", data_to_update)

    merged_status = {
        "name": old_status.name,
        "phase_id": old_status.phase.id
    }

    merged_status.update(data_to_update)

    sql = '''UPDATE status SET name = ?, phase_id = ? WHERE id = ?'''

    cursor = conn.cursor()

    cursor.execute(sql,
                   (merged_status["name"], merged_status["phase_id"], id)
                   )

    conn.commit()

    result = get_status_by_id(id, conn)
    print(f"Result after update: {result}")
    return result
