import sqlite3


def _map_row_to_application(row) ->dict:
    return {
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


def get_all_applications(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute('''
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
                ''')
                
    rows = cursor.fetchall()

    return [_map_row_to_application(row) for row in rows]
    
