import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')

def execute_and_commit_insert(conn, sql, entry):
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    
    return cur.lastrowid


def get_phase_id_by_name(conn, name):
    sql = '''SELECT id FROM phase WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, name)
    row = cur.fetchone()
    
    return row[0]


def get_status_id_by_name(conn, name):
    sql = '''SELECT id FROM status WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, name)
    row = cur.fetchone()
    
    return row[0]


def add_phase(conn, phase):
    sql = ''' INSERT OR IGNORE INTO phase(name)
              VALUES(?) '''
    
    execute_and_commit_insert(conn, sql, phase)


def add_status(conn, status):
    sql = ''' INSERT INTO status(name,phase_id)
              VALUES(?,?) '''
    
    execute_and_commit_insert(conn, sql, status)
    

def add_application(conn, application):
    sql = ''' INSERT INTO application(company_name,job_title,URL,status_id,date_added,date_appointment)
              VALUES(?,?,?,?,?,?) '''
    
    execute_and_commit_insert(conn, sql, application)


def main():
    if not DATABASE_NAME:
        raise ValueError("DATABASE_NAME not found in environment")

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            phases = [
                ('Review',),
                ('Interviewing',),
                ('Decision',),
                ('Closed',),
            ]
            for phase in phases:
                phase_id = add_phase(conn,phase)
                print(f'Created a phase with the id {phase_id}')

            states = [
                ('Applied', get_phase_id_by_name(conn, ('Review',))),
                ('Job Interview', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Technical Assessment', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Phone Interview', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Online Assessment', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Behavioral Assessment', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Home Assignment', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Cognitive Assessment', get_phase_id_by_name(conn, ('Interviewing',))),
                ('Offer Extended', get_phase_id_by_name(conn, ('Decision',))),
                ('Offer Declined', get_phase_id_by_name(conn, ('Closed',))),
                ('Rejected', get_phase_id_by_name(conn, ('Closed',))),
                ('Offer Accepted', get_phase_id_by_name(conn, ('Closed',))),
            ]

            for status in states:
                status_id = add_status(conn,status)
                print(f'Created a status with the id {status_id}')

            applications = [
                ('Test Firma', 'Test Job: Entwickler (m,w,d)','',get_status_id_by_name(conn, ('Applied',)),'2026-01-01', '2026-01-02'),
                ('Test Firma2', 'Test Job: Fullstack-Entwickler (m,w,d)','',get_status_id_by_name(conn, ('Job Interview',)),'2026-02-10', '2026-03-21'),
                ('Test Firma3', 'Test Job: Java-Entwickler (m,w,d)','',get_status_id_by_name(conn, ('Rejected',)),'2026-03-11', '2026-05-09')
            ]

            for application in applications:
                application_id = add_application(conn,application)
                print(f'Created Application {application_id}')

    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    main()