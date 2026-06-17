import sqlite3
from database import get_db


def update_empty_url_str_to_none(conn: sqlite3.Connection):
    sql = '''UPDATE application
             SET URL = NULL
             WHERE URL = ""
          '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    row = cur.rowcount

    print(row)


def check_affected_rows(conn: sqlite3.Connection):
    sql = '''SELECT COUNT(*) FROM application WHERE URL = "" '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    rows = cur.fetchone()[0]

    print(rows)


if __name__ == "__main__":

    db_gen = get_db()
    conn = next(db_gen)

    update_empty_url_str_to_none(conn)
    # check_affected_rows(conn)
