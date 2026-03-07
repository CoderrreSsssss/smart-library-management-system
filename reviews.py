from database import connect_db
from reviews import add_review, get_reviews
def add_review(book_id, rating, review):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reviews(book_id,rating,review) VALUES(?,?,?)",
        (book_id, rating, review)
    )

    conn.commit()


def get_reviews(book_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT rating,review FROM reviews WHERE book_id=?",
        (book_id,)
    )

    return cursor.fetchall()
