## SQLite Handling ##
import sqlite3
import os.path

def createTables():
    DB.execute("""
        CREATE TABLE 'config' (
        'folder' TEXT
        )
    """)

    DB.execute("""
        CREATE TABLE 'downloaded' (
        'work' INTEGER,
        'series' INTEGER
        )
    """)

    DB.execute("""
        CREATE TABLE 'works' (
        'work' INTEGER,
        )
    """)

    DB.execute("""
        CREATE TABLE 'series' (
        'work' INTEGER,
        'series' INTEGER
        )
    """)

if __name__ == "__main__":
    connect = sqlite3.connect("bookmarks.db")
    DB = connect.cursor()
    populated = DB.execute("SELECT name FROM sqlite_master")

    if populated.fetchone() == None:
        createTables()
    connect.close()
