from database import connect_db
from datetime import date

def issue_book(user_id,book_id):

    conn = connect_db()
    c = conn.cursor()

    c.execute(
    "INSERT INTO borrow(user_id,book_id,issue_date) VALUES(?,?,?)",
    (user_id,book_id,str(date.today()))
    )

    conn.commit()


def return_book(book_id):

    conn = connect_db()
    c = conn.cursor()

    c.execute(
    "UPDATE borrow SET return_date=? WHERE book_id=?",
    (str(date.today()),book_id)
    )

    conn.commit()


def get_all_issued():

    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    SELECT users.name,books.title,borrow.issue_date,borrow.return_date
    FROM borrow
    JOIN users ON borrow.user_id=users.id
    JOIN books ON borrow.book_id=books.id
    """)

    return c.fetchall()
