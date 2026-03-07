from database import connect_db

def borrow_book(user_id,book_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO borrow(user_id,book_id) VALUES(?,?)",
    (user_id,book_id)
    )

    conn.commit()
