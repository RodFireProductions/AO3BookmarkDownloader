## SQLite Handling ##
import sqlite3
import os.path

##
def createTables():
    DB.execute("""
        CREATE TABLE 'config' (
        'folder' TEXT
        )
    """)

    DB.execute("""
        CREATE TABLE 'downloaded' (
        'work' INTEGER,
        'series' INTEGER,
        'work_title' TEXT,
        'series_title' TEXT
        )
    """)

    DB.execute("""
        CREATE TABLE 'works' (
        'work' INTEGER,
        'title' TEXT
        )
    """)

    DB.execute("""
        CREATE TABLE 'series' (
        'series' INTEGER,
        'title' TEXT
        )
    """)

##
def insertWork(id, title):
    data = [( id, title )]
    db = connectDB()
    db["cur"].executemany("INSERT INTO works VALUES(?, ?)", data)
    db["con"].commit()
    db["con"].close()

def insertSeries(id, title):
    data = [( id, title )]
    db = connectDB()
    db["cur"].executemany("INSERT INTO series VALUES(?, ?)", data)
    db["con"].commit()
    db["con"].close()

def insertDownloaded(w_id, s_id, w_title, s_title):
    data = [( w_id, s_id, w_title, s_title )]
    db = connectDB()
    db["cur"].executemany("INSERT INTO downloaded VALUES(?, ?, ?, ?)", data)
    db["con"].commit()
    db["con"].close()

##
def removeWork(id):
    db = connectDB()

def removeSeries(id):
    db = connectDB()

def removeAllDownloaded():
    db = connectDB()

def removeAllWork():
    db = connectDB()

def removeAllSeries():
    db = connectDB()

##
def connectDB():
    con = sqlite3.connect("bookmarks.db")
    return {
        "con": con,
        "cur": con.cursor()
    }

##
connect = sqlite3.connect("bookmarks.db")
DB = connect.cursor()
populated = DB.execute("SELECT name FROM sqlite_master")

if populated.fetchone() == None:
    createTables()
    connect.commit()
connect.close()
