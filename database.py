import sqlite3

def connect_db():
    conn = sqlite3.connect("library.db",check_same_thread=False)
    return conn

def create_tables():

    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    genre TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS borrow(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    return_date TEXT
    )
    """)

    conn.commit()
