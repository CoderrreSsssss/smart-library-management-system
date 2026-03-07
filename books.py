from database import connect_db

def add_book(title,author,genre):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO books(title,author,genre) VALUES(?,?,?)",
    (title,author,genre)
    )

    conn.commit()


def get_books():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")

    return cursor.fetchall()
