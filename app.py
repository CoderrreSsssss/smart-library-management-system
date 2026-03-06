import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Library System", layout="wide")

st.title("📚 Smart Library Management System")

# session storage
if "books" not in st.session_state:
    st.session_state.books = []

if "students" not in st.session_state:
    st.session_state.students = []

if "issued" not in st.session_state:
    st.session_state.issued = []

menu = ["Dashboard","Add Book","View Books","Add Student","Issue Book","Return Book"]

choice = st.sidebar.selectbox("Menu",menu)

# DASHBOARD
if choice == "Dashboard":

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Books", len(st.session_state.books))
    col2.metric("Total Students", len(st.session_state.students))
    col3.metric("Books Issued", len(st.session_state.issued))

# ADD BOOK
elif choice == "Add Book":

    st.subheader("Add New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")

    if st.button("Add Book"):

        st.session_state.books.append({
            "Title":title,
            "Author":author
        })

        st.success("Book Added Successfully")

# VIEW BOOKS
elif choice == "View Books":

    st.subheader("Library Books")

    if len(st.session_state.books) > 0:

        df = pd.DataFrame(st.session_state.books)

        search = st.text_input("Search Book")

        if search:
            df = df[df["Title"].str.contains(search,case=False)]

        st.dataframe(df)

    else:
        st.info("No books available")

# ADD STUDENT
elif choice == "Add Student":

    name = st.text_input("Student Name")

    if st.button("Add Student"):

        st.session_state.students.append(name)

        st.success("Student Added")

# ISSUE BOOK
elif choice == "Issue Book":

    if st.session_state.books and st.session_state.students:

        book = st.selectbox("Select Book",[b["Title"] for b in st.session_state.books])
        student = st.selectbox("Select Student",st.session_state.students)

        if st.button("Issue"):

            st.session_state.issued.append({
                "Book":book,
                "Student":student
            })

            st.success("Book Issued")

# RETURN BOOK
elif choice == "Return Book":

    if st.session_state.issued:

        df = pd.DataFrame(st.session_state.issued)

        book = st.selectbox("Select Book to Return",df["Book"])

        if st.button("Return"):

            st.session_state.issued = [
                i for i in st.session_state.issued if i["Book"] != book
            ]

            st.success("Book Returned")
