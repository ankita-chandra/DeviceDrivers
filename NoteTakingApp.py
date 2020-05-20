# ==========================================
# Title:  Device Driver Assignment
# Author: Ankita Chandra
# Date:   13 March 2020
# ==========================================

import argparse
import os

# Details of the Database -------------------------

DB_TABLE = 'notes'
DATABASE = 'MyPocket'
DB_HOST = 'Ankitaa'
DB_USER = 'Ankitaa'
DB_PASSWORD = 'sherlock'
DATABASE_TYPE = 'sqlite'

# -------------------------------------------------



# Connecting Database-----------------------------

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

# ------------------------------------------------



# Creating Tables------------------------------

def create_sqlite_tables(conn):
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()

# ---------------------------------------------



# Insert Entries into Table------------------------------------

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

# ----------------------------------------------------------------



# Read Entries from Table-------------------------------------------

def read_from_db():
    x=0
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
            x=1
        if x==0:
            print('There is no entry stored')
    except:
        print("Error: unable to fetch data")

    connect.close()

# ---------------------------------------------------------------------



# Modify Data Present In the Table-----------------------------------------

def modify_data(idx, modified_note):
    connect = get_database_connection()
    cursor = connect.cursor()
    updateQuery = 'UPDATE ' + DB_TABLE + ' SET note = "' + modified_note + '" WHERE id = ' + idx
    try:
        cursor.execute(updateQuery)
        connect.commit()
        print('Successfully modified the note.')
    except:
        print("Error: unable to fetch data")
        connect.rollback()
    connect.close()

# --------------------------------------------------------------------------



# Update Tag of an Entry------------------------------------------------------

def update_tag(idx, modified_tag):
    connect = get_database_connection()
    cursor = connect.cursor()
    updateQuery = 'UPDATE ' + DB_TABLE + ' SET tags = "' + modified_tag + '" WHERE id = ' + idx
    try:
        cursor.execute(updateQuery)
        connect.commit()
        print('Successfully modified the note.')
    except:
        print("Error: unable to fetch data")
        connect.rollback()
    connect.close()

# ----------------------------------------------------------------------------------



# Read Tags and Print Them---------------------------------------------------------

def read_tags():
    connect = get_database_connection()
    cursor = connect.cursor()
    readQuery = 'SELECT DISTINCT tags FROM ' + DB_TABLE
    try:
        cursor.execute(readQuery)
        results = cursor.fetchall()
        print('Tags:')
        for row in results:
            tags = row[0]
            print(tags)

    except:
        print("Error: unable to fetch data")
    connect.close()

# ---------------------------------------------------------------------------------



# Delete an Entry Using ID--------------------------------------------------------

def delete_using_id(idx):
    connect = get_database_connection()
    cursor = connect.cursor()
    deleteQuery = 'DELETE  FROM ' + DB_TABLE + ' WHERE id = ' + idx
    try:
        cursor.execute(deleteQuery)
        connect.commit()
        print('Successfully deleted the note.')
    except:
        print("Something went wrong try again")
        connect.rollback()
    connect.close()

# ------------------------------------------------------------------------------



# Search Entry Using Tags-------------------------------------------------------

def search_using_tags(pattern):
    connect = get_database_connection()
    cursor = connect.cursor()
    searchNoteUsingTagQuery = 'SELECT * FROM ' + DB_TABLE + ' WHERE tags LIKE "%' + pattern + '%"'
    try:
        cursor.execute(searchNoteUsingTagQuery)
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

# ------------------------------------------------------------------------------



# Read and Print All The Entries------------------------------------------------

def read_clean():
    connect = get_database_connection()
    cursor = connect.cursor()
    readQuery = 'SELECT * FROM ' + DB_TABLE
    try:
        cursor.execute(readQuery)
        results = cursor.fetchall()
        for row in simple_generator(results):
            print(row)
    except:
        print("Error: unable to fetch data")
    connect.close()

# ---------------------------------------------------------------------------------



# Set Reminder--------------------------------------------------------------------

def reminder(message, date):
    with open('/home/ankita/DeviceDrivers/Schedules.txt', 'a') as outFile:
        outFile.write(date + ' ' + message + '\n')
    print('Reminder set Successfully')

# --------------------------------------------------------------------------------



# Print the Data of a givenn Row----------------------------------------------------

def print_data(row):
    print()
    print('ID:', row[0])
    print('Created At:', row[1])
    print('Last Modified At:', row[2])
    print('Note:', row[3])
    print('Tag:', row[4])
    return

# ------------------------------------------------------------------------------------



# Check the Arguments Passed------------------------------------------------------------

def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add_note', nargs='*', help='Add notes to the database', action='store')
    parser.add_argument('-r', '--read_all', help='Fetch all Records from the database', action='store_true')
    parser.add_argument('-u', '--update', nargs='*', help='Update a record from the database', action='store')
    parser.add_argument('-ut', '--update_tag', nargs='*', help='Update a tag of a record from the database',action='store')
    parser.add_argument('-rt', '--read_tags', help='Read all the available tags from database', action='store_true')
    parser.add_argument('-d', '--delete', help='Delete a record from database', action='store')
    parser.add_argument('-st', '--search_using_tags', help='Search notes based on tags', action='store')
    parser.add_argument('-rc', '--read_clean', help='Fetch all Records one by one from the database',action='store_true')
    parser.add_argument('--reminder', nargs='*', help='Set a reminder', action='store')
    
    arg = parser.parse_args()
    if (arg.add_note):
        try:
            insert_into_db(arg.add_note[0], arg.add_note[1])
        except IndexError:
            print('You have to give two values [NOTE, TAGS]')

    elif (arg.read_all):
        read_from_db()

    elif (arg.update):
        try:
            modify_data(arg.update[0], arg.update[1])
        except:
            print('You have to give two values [ID, MODIFIED TEXT]')

    elif (arg.update_tag):
        try:
            update_tag(arg.update_tag[0], arg.update_tag[1])
        except:
            print('You have to give two values [ID, MODIFIED TAG]')

    elif (arg.delete):
        delete_using_id(arg.delete)

    elif (arg.read_clean):
        read_clean()

    elif (arg.search_using_tags):
        search_using_tags(arg.search_using_tags)

    elif (arg.read_tags):
        read_tags()

    elif (arg.reminder):
        try:
            reminder(arg.reminder[0], arg.reminder[1])
        except:
            print('You have to give two values [REMINDER TEXT, "DATE(dd-mm-yyyy) TIME(hh:ss)"]')

    else:
        print('Reading Data from Database..')
        read_from_db()

# -----------------------------------------------------------------------------------------



# Initiate the Program---------------------------------

if __name__ == '__main__':
    argumentParser()
    
# -------------------------------------------------------