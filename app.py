import streamlit as st
import sqlite3
from datetime import date

# ---------- DATABASE ----------

conn = sqlite3.connect("library.db",check_same_thread=False)
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

# ---------- UI DESIGN ----------

st.set_page_config(page_title="Smart Library",layout="wide")

st.markdown("""
<style>

.stApp{
background: linear-gradient(to right,#0f2027,#203a43,#2c5364);
color:white;
}

button{
background-color:#00c6ff;
color:white;
}

</style>
""",unsafe_allow_html=True)

# ---------- SESSION ----------

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "role" not in st.session_state:
    st.session_state.role=None

if "user_id" not in st.session_state:
    st.session_state.user_id=None

# ---------- REGISTER ----------

def register():

    st.subheader("📝 Register")

    name=st.text_input("Name")
    email=st.text_input("Email")
    password=st.text_input("Password",type="password")

    if st.button("Register"):

        c.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
        (name,email,password,"student"))

        conn.commit()

        st.success("Account Created! Please Login")

# ---------- LOGIN ----------

def login():

    st.subheader("🔑 Login")

    email=st.text_input("Email")
    password=st.text_input("Password",type="password")

    if st.button("Login"):

        c.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password))

        user=c.fetchone()

        if user:

            st.session_state.logged_in=True
            st.session_state.role=user[4]
            st.session_state.user_id=user[0]

            st.success("Login Successful")

        else:

            st.error("Invalid Credentials")

# ---------- STUDENT DASHBOARD ----------

def student_dashboard():

    st.title("📚 Student Library Dashboard")

    search=st.text_input("🔎 Search Books")

    c.execute("SELECT * FROM books")
    books=c.fetchall()

    for book in books:

        if search.lower() in book[1].lower():

            st.subheader(book[1])
            st.write("Author:",book[2])
            st.write("Genre:",book[3])

            if st.button(f"Issue Book {book[0]}"):

                c.execute(
                "INSERT INTO borrow(user_id,book_id,issue_date) VALUES(?,?,?)",
                (st.session_state.user_id,book[0],str(date.today()))
                )

                conn.commit()

                st.success("Book Issued!")

    st.subheader("📖 My Issued Books")

    c.execute("""
    SELECT books.title,borrow.issue_date,borrow.return_date,borrow.book_id
    FROM borrow
    JOIN books ON books.id=borrow.book_id
    WHERE borrow.user_id=?
    """,(st.session_state.user_id,))

    issued=c.fetchall()

    for book in issued:

        st.write("📚",book[0])
        st.write("Issue Date:",book[1])
        st.write("Return Date:",book[2])

        if book[2] is None:

            if st.button(f"Return {book[3]}"):

                c.execute(
                "UPDATE borrow SET return_date=? WHERE book_id=?",
                (str(date.today()),book[3])
                )

                conn.commit()

                st.success("Book Returned")

# ---------- ADMIN PANEL ----------

def admin_panel():

    st.title("🛠 Admin Panel")

    st.subheader("➕ Add Book")

    title=st.text_input("Book Title")
    author=st.text_input("Author")
    genre=st.text_input("Genre")

    if st.button("Add Book"):

        c.execute(
        "INSERT INTO books(title,author,genre) VALUES(?,?,?)",
        (title,author,genre)
        )

        conn.commit()

        st.success("Book Added")

    st.subheader("📚 Manage Books")

    c.execute("SELECT * FROM books")
    books=c.fetchall()

    for book in books:

        st.write(book)

        if st.button(f"Delete {book[0]}"):

            c.execute("DELETE FROM books WHERE id=?",(book[0],))
            conn.commit()

            st.warning("Book Deleted")

    st.subheader("📊 Issued Books")

    c.execute("""
    SELECT users.name,books.title,borrow.issue_date,borrow.return_date
    FROM borrow
    JOIN users ON borrow.user_id=users.id
    JOIN books ON borrow.book_id=books.id
    """)

    data=c.fetchall()

    for row in data:

        st.write("Student:",row[0])
        st.write("Book:",row[1])
        st.write("Issued:",row[2])
        st.write("Returned:",row[3])
        st.write("-------------------")

# ---------- MAIN APP ----------

st.title("📚 Smart Library System")

menu=st.sidebar.selectbox("Menu",["Login","Register"])

if not st.session_state.logged_in:

    if menu=="Login":
        login()

    if menu=="Register":
        register()

else:

    if st.session_state.role=="student":

        student_dashboard()

    else:

        admin_panel()
