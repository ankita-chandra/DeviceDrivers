# ==========================================
# Title:  Device Driver Assignment
# Author: Ankita Chandra
# Date:   13 March 2020
# ==========================================

import argparse
import os

DB_TABLE = 'notes'
DATABASE = 'MyPocket'
DB_HOST = 'Ankitaa'
DB_USER = 'Ankitaa'
DB_PASSWORD = 'sherlock'
DATABASE_TYPE = 'sqlite'


def get_database_connection():
    if DATABASE_TYPE == 'mysql':
        import pymysql
        return pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_TABLE)
    elif DATABASE_TYPE == 'postgresql':
        import psycopg2
        conn = psycopg2.connect(
            database=DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=PORT
        )
        return conn
    elif DATABASE_TYPE == 'sqlite':
        import sqlite3
        sqlite_file = 'notes.db'
        file_exists = os.path.isfile(sqlite_file)
        conn = sqlite3.connect(sqlite_file)
        if not file_exists:
            create_sqlite_tables(conn)
        return conn
    else:
        raise Exception("Undefined database type!")


def create_sqlite_tables(conn):
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()


def insert_into_db(note, tags):
    connection = get_database_connection()
    cursor = connection.cursor()
    insertQuery = "INSERT INTO " + DB_TABLE + "(note, tags) VALUES ('" + note + "', '" + tags + "')"
    try:
        cursor.execute(insertQuery)
        connection.commit()
        print('Successful inserted new note.')
    except:
        connection.rollback()
    connection.close()


def read_from_db():
    connect = get_database_connection()
    cursor = connect.cursor()
    readQuery = 'SELECT * FROM ' + DB_TABLE
    try:
        cursor.execute(readQuery)
        results = cursor.fetchall()

        for row in results:
            ID = row[0]
            createdAt = row[1]
            modifiedAt = row[2]
            Note = row[3]
            Tag = row[4]

            print()
            print('ID:', ID)
            print('Created At:', createdAt)
            print('Last Modified At:', modifiedAt)
            print('Note:', Note)
            print('Tag:', Tag)
    except:
        print("Error: unable to fetch data")

    connect.close()

def print_data(row):
    print()
    print('ID:', row[0])
    print('Created At:', row[1])
    print('Last Modified At:', row[2])
    print('Note:', row[3])
    print('Tag:', row[4])
    return

def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add_note', nargs='*', help='Add notes to the database', action='store')
    parser.add_argument('-r', '--read_all', help='Fetch all Records from the database', action='store_true')
    arg = parser.parse_args()
    if (arg.add_note):
        try:
            insert_into_db(arg.add_note[0], arg.add_note[1])
        except IndexError:
            print('You have to give two values [NOTE, TAGS]')
    elif (arg.read_all):
        read_from_db()
    else:
        print('Reading Data from Database..')
        read_from_db()

if __name__ == '__main__':
    argumentParser()
