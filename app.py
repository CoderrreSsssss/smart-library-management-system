import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import datetime

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("library.db",check_same_thread=False)
c = conn.cursor()

def create_tables():

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    category TEXT)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS borrow(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    return_date TEXT)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    rating INTEGER,
    review TEXT)
    """)

    conn.commit()

create_tables()

# ---------------- PASSWORD HASH ---------------- #

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- DEFAULT BOOKS ---------------- #

def add_default_books():

    c.execute("SELECT COUNT(*) FROM books")
    count=c.fetchone()[0]

    if count==0:

        books=[
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
            for b in books:
                c.execute("INSERT INTO books(title,author,category) VALUES(?,?,?)",b)

        conn.commit()

add_default_books()

# ---------------- LOGIN ---------------- #

def login():

    st.title("📚 Smart Library Login")

    email=st.text_input("Email")
    password=st.text_input("Password",type="password")

    if st.button("Login"):

        password=hash_password(password)

        c.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        user=c.fetchone()

        if user:

            st.session_state.logged=True
            st.session_state.user_id=user[0]
            st.session_state.role=user[4]
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid credentials")

# ---------------- REGISTER ---------------- #

def register():

    st.title("📚 Register")

    name=st.text_input("Name")
    email=st.text_input("Email")
    password=st.text_input("Password",type="password")

    if st.button("Register"):

        password=hash_password(password)

        try:
            c.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (name,email,password,"student"))
            conn.commit()

            st.success("Account Created!")

        except:
            st.error("Email already registered")

# ---------------- ADMIN DASHBOARD ---------------- #

def admin_dashboard():

    st.title("👑 Admin Dashboard")

    menu=st.sidebar.selectbox("Menu",
    ["Analytics","Add Book","Remove Book","All Books","Issued Books"])

    if menu=="Analytics":

        st.subheader("📊 Library Analytics")

        books=pd.read_sql_query("SELECT * FROM books",conn)
        borrow=pd.read_sql_query("SELECT * FROM borrow",conn)

        st.metric("Total Books",len(books))
        st.metric("Total Issued",len(borrow))

        if not books.empty:
            st.bar_chart(books["category"].value_counts())

    elif menu=="Add Book":

        st.subheader("➕ Add Book")

        title=st.text_input("Title")
        author=st.text_input("Author")
        category=st.text_input("Category")

        if st.button("Add"):

            c.execute("INSERT INTO books(title,author,category) VALUES(?,?,?)",
            (title,author,category))

            conn.commit()
            st.success("Book Added")

    elif menu=="Remove Book":

        st.subheader("❌ Remove Book")

        books=pd.read_sql_query("SELECT * FROM books",conn)

        book=st.selectbox("Select Book",books["title"])

        if st.button("Delete"):

            c.execute("DELETE FROM books WHERE title=?",(book,))
            conn.commit()

            st.success("Book Deleted")

    elif menu=="All Books":

        st.subheader("📚 All Books")

        books=pd.read_sql_query("SELECT * FROM books",conn)
        st.dataframe(books)

    elif menu=="Issued Books":

        st.subheader("📖 Borrow Records")

        data=pd.read_sql_query("""
        SELECT users.name,books.title,borrow.issue_date,borrow.return_date
        FROM borrow
        JOIN users ON borrow.user_id=users.id
        JOIN books ON borrow.book_id=books.id
        """,conn)

        st.dataframe(data)

# ---------------- STUDENT DASHBOARD ---------------- #

def student_dashboard():

    st.title("📚 Student Library")

    menu=st.sidebar.selectbox("Menu",
    ["Browse Books","My Books","Search","Recommend"])

    if menu=="Browse Books":

        books=pd.read_sql_query("SELECT * FROM books",conn)

        for i,row in books.iterrows():

            st.subheader(row["title"])
            st.write(row["author"],"|",row["category"])

            if st.button("Issue",key=row["id"]):

                c.execute("""
                INSERT INTO borrow(user_id,book_id,issue_date,return_date)
                VALUES(?,?,?,?)
                """,
                (st.session_state.user_id,row["id"],datetime.today().date(),"Not Returned"))

                conn.commit()

                st.success("Book Issued")

    elif menu=="My Books":

        data=pd.read_sql_query("""
        SELECT books.title,borrow.issue_date,borrow.return_date,borrow.book_id
        FROM borrow
        JOIN books ON borrow.book_id=books.id
        WHERE borrow.user_id=?
        """,conn,params=(st.session_state.user_id,))

        st.dataframe(data)

        for i,row in data.iterrows():

            if row["return_date"]=="Not Returned":

                if st.button("Return "+row["title"],key=i):

                    c.execute("""
                    UPDATE borrow
                    SET return_date=?
                    WHERE user_id=? AND book_id=? AND return_date='Not Returned'
                    """,
                    (datetime.today().date(),
                    st.session_state.user_id,row["book_id"]))

                    conn.commit()
                    st.success("Returned")

    elif menu=="Search":

        q=st.text_input("Search Books")

        if q:

            data=pd.read_sql_query("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
            """,conn,params=(f"%{q}%",f"%{q}%",f"%{q}%"))

            st.dataframe(data)

    elif menu=="Recommend":

        st.subheader("🤖 AI Book Recommendation")

        books=pd.read_sql_query("SELECT * FROM books",conn)

        cat=st.selectbox("Select Category",books["category"].unique())

        rec=books[books["category"]==cat]

        st.write("Recommended Books")

        st.dataframe(rec[["title","author"]])

# ---------------- SESSION ---------------- #

if "logged" not in st.session_state:
    st.session_state.logged=False

# ---------------- MAIN ---------------- #

if not st.session_state.logged:

    choice=st.sidebar.selectbox("Menu",["Login","Register"])

    if choice=="Login":
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
