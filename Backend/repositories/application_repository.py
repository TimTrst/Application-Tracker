import sqlite3
from models.application import WriteApplication, UpdateApplication, ReadApplication, BaseApplication
import datetime

BASE_APPLICATION_QUERY = '''
                SELECT
                    application.id as id,
                    application.company_name as company_name,
                    application.job_title as job_title,
                    application.URL as url,
                    status.id as status_id,
                    status.name as status_name,
                    phase.name as phase_name,
                    application.date_added as date_added,
                    application.date_appointment as date_appointment
                FROM application
                    LEFT JOIN status ON application.status_id = status.id
                    LEFT JOIN phase ON status.phase_id = phase.id
                '''


def _map_row_to_application(row) -> ReadApplication:
    application = {
        "id": row["id"],
        "company_name": row["company_name"],
        "job_title": row["job_title"],
        "url": row["url"],
        "status": {
            "id": row["status_id"],
            "name": row["status_name"],
            "phase": {
                "name": row["phase_name"],
            }
        },
        "date_added": row["date_added"],
        "date_appointment": row["date_appointment"]
    }

    return ReadApplication.model_validate(application)


def get_all_applications(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(BASE_APPLICATION_QUERY)

    rows = cursor.fetchall()

    return [_map_row_to_application(row) for row in rows]


def get_application_by_id(id, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(BASE_APPLICATION_QUERY +
                   '''WHERE application.id = ?''', (id, ))

    row = cursor.fetchone()

    if not row:
        return None

    return _map_row_to_application(row)


def add_application(new_application: WriteApplication, conn: sqlite3.Connection):
    sql = ''' INSERT INTO application(company_name,job_title,URL,status_id,date_added,date_appointment)
              VALUES(?,?,?,?,?,?) '''

    cursor = conn.cursor()
    cursor.execute(sql,
                   (new_application.company_name,
                    new_application.job_title,
                    new_application.url,
                    new_application.status_id,
                    datetime.datetime.now().date(),
                    new_application.date_appointment)
                   )

    conn.commit()

    new_id = cursor.lastrowid

    return get_application_by_id(new_id, conn)


def remove_application(id: int, conn: sqlite3.Connection):
    sql = '''DELETE FROM application WHERE id = ?'''

    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False
    return True


def modify_application(id: int, updated_application: UpdateApplication, conn: sqlite3.Connection):
    data_to_update = updated_application.model_dump(exclude_unset=True)

    if not data_to_update:
        return False

    old_application = get_application_by_id(id, conn)

    merged_application = {
        "company_name": old_application.company_name,
        "job_title": old_application.job_title,
        "url": old_application.url,
        "status_id": old_application.status.id,
        "date_appointment": old_application.date_appointment
    }

    merged_application.update(data_to_update)

    sql = '''UPDATE application SET company_name = ?, job_title = ?, URL = ?, status_id = ?, date_appointment = ? WHERE id = ?'''

    cursor = conn.cursor()

    cursor.execute(sql,
                   (merged_application["company_name"],
                    merged_application["job_title"],
                    merged_application["url"],
                    merged_application["status_id"],
                    merged_application["date_appointment"], id)
                   )

    conn.commit()

    result = get_application_by_id(id, conn)
    print(f"Result after update: {result}")
    return result
