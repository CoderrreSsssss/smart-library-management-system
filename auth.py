from database import connect_db

def register(name,email,password):

    conn = connect_db()
    c = conn.cursor()

    c.execute(
    "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
    (name,email,password,"student")
    )

    conn.commit()


def login(email,password):

    conn = connect_db()
    c = conn.cursor()

    c.execute(
    "SELECT * FROM users WHERE email=? AND password=?",
    (email,password)
    )

    return c.fetchone()
