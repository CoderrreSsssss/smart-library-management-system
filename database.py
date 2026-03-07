import sqlite3

def connect_db():
    conn = sqlite3.connect("library.db")
    return conn


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    genre TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    rating INTEGER,
    review TEXT
    )
    """)

    conn.commit()
    conn.close()
