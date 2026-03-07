import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("library.db", check_same_thread=False)
c = conn.cursor()

def init_db():

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        category TEXT
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

init_db()

# ---------------- PASSWORD HASH ---------------- #

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- DEFAULT BOOKS ---------------- #

def seed_books():

    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]

    if count == 0:

        books = [
        ("Atomic Habits","James Clear","Self Help"),
        ("Rich Dad Poor Dad","Robert Kiyosaki","Finance"),
        ("Deep Work","Cal Newport","Productivity"),
        ("The Alchemist","Paulo Coelho","Fiction"),
        ("Harry Potter","J.K Rowling","Fantasy"),
        ("Think and Grow Rich","Napoleon Hill","Success"),
        ("Psychology of Money","Morgan Housel","Finance"),
        ("Ikigai","Hector Garcia","Self Help"),
        ("Sapiens","Yuval Noah Harari","History"),
        ("Zero to One","Peter Thiel","Startup")
        ]

        for i in range(5):
            for title,author,category in books:
                c.execute(
                "INSERT INTO books(title,author,category) VALUES(?,?,?)",
                (title,author,category)
                )

        conn.commit()

seed_books()

# ---------------- LOGIN ---------------- #

def login():

    st.title("📚 Smart Library Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        hashed = hash_password(password)

        c.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,hashed)
        )

        user = c.fetchone()

        if user:
            st.session_state.logged = True
            st.session_state.user_id = user[0]
            st.session_state.role = user[4]
            st.rerun()

        else:
            st.error("Invalid login")

# ---------------- REGISTER ---------------- #

def register():

    st.title("Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        try:

            hashed = hash_password(password)

            c.execute(
            "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (name,email,hashed,"student")
            )

            conn.commit()

            st.success("Account created")

        except:
            st.error("Email already exists")

# ---------------- ADMIN ---------------- #

def admin_dashboard():

    st.title("👑 Admin Panel")

    menu = st.sidebar.selectbox(
    "Menu",
    ["Add Book","Remove Book","View Books","Borrow Records"]
    )

    if menu=="Add Book":

        title = st.text_input("Title")
        author = st.text_input("Author")
        category = st.text_input("Category")

        if st.button("Add"):

            c.execute(
            "INSERT INTO books(title,author,category) VALUES(?,?,?)",
            (title,author,category)
            )

            conn.commit()

            st.success("Book added")

    elif menu=="Remove Book":

        c.execute("SELECT id,title FROM books")
        books = c.fetchall()

        titles = [b[1] for b in books]

        selected = st.selectbox("Book", titles)

        if st.button("Delete"):

            c.execute(
            "DELETE FROM books WHERE title=?",
            (selected,)
            )

            conn.commit()

            st.success("Book deleted")

    elif menu=="View Books":

        c.execute("SELECT * FROM books")
        data = c.fetchall()

        st.write(data)

    elif menu=="Borrow Records":

        c.execute("""
        SELECT users.name,books.title,borrow.issue_date,borrow.return_date
        FROM borrow
        JOIN users ON users.id=borrow.user_id
        JOIN books ON books.id=borrow.book_id
        """)

        data = c.fetchall()

        st.write(data)

# ---------------- STUDENT ---------------- #

def student_dashboard():

    st.title("📖 Student Library")

    menu = st.sidebar.selectbox(
    "Menu",
    ["Browse Books","My Books","Search"]
    )

    if menu=="Browse Books":

        c.execute("SELECT * FROM books")
        books = c.fetchall()

        for book in books:

            st.subheader(book[1])
            st.write(book[2],"|",book[3])

            if st.button("Issue", key=book[0]):

                c.execute("""
                INSERT INTO borrow(user_id,book_id,issue_date,return_date)
                VALUES(?,?,?,?)
                """,
                (
                st.session_state.user_id,
                book[0],
                str(datetime.today().date()),
                "Not Returned"
                )
                )

                conn.commit()

                st.success("Book issued")

    elif menu=="My Books":

        c.execute("""
        SELECT books.title,borrow.issue_date,borrow.return_date
        FROM borrow
        JOIN books ON books.id=borrow.book_id
        WHERE borrow.user_id=?
        """,
        (st.session_state.user_id,)
        )

        data = c.fetchall()

        st.write(data)

    elif menu=="Search":

        q = st.text_input("Search")

        if q:

            c.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ?
            """,
            (f"%{q}%",f"%{q}%")
            )

            data = c.fetchall()

            st.write(data)

# ---------------- SESSION ---------------- #

if "logged" not in st.session_state:
    st.session_state.logged=False

# ---------------- MAIN ---------------- #

if not st.session_state.logged:

    menu = st.sidebar.selectbox("Menu",["Login","Register"])

    if menu=="Login":
        login()
    else:
        register()

else:

    if st.session_state.role=="admin":
        admin_dashboard()
    else:
        student_dashboard()

    if st.sidebar.button("Logout"):
        st.session_state.logged=False
        st.rerun()
