from database import connect_db

def add_book(title,author,genre):

    conn = connect_db()
    c = conn.cursor()

    c.execute(
    "INSERT INTO books(title,author,genre) VALUES(?,?,?)",
    (title,author,genre)
    )

    conn.commit()


def delete_book(book_id):

    conn = connect_db()
    c = conn.cursor()

    c.execute("DELETE FROM books WHERE id=?",(book_id,))
    conn.commit()


def get_books():

    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT * FROM books")

    return c.fetchall()
