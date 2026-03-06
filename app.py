import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from login import login

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

st.title("📚 Smart Library Management System")

# storage
if "books" not in st.session_state:
    st.session_state.books = []

if "students" not in st.session_state:
    st.session_state.students = []

if "issued" not in st.session_state:
    st.session_state.issued = []

menu = ["Dashboard","Books","Students","Issue Book","Return Book"]

choice = st.sidebar.selectbox("Menu",menu)

# DASHBOARD
if choice == "Dashboard":

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Books",len(st.session_state.books))
    col2.metric("Total Students",len(st.session_state.students))
    col3.metric("Books Issued",len(st.session_state.issued))

    if st.session_state.books:

        df = pd.DataFrame(st.session_state.books)

        chart = px.histogram(df,x="Author")

        st.plotly_chart(chart)

# BOOKS
elif choice == "Books":

    st.subheader("Add Book")

    title = st.text_input("Title")
    author = st.text_input("Author")

    image = st.file_uploader("Book Cover")

    if st.button("Add Book"):

        st.session_state.books.append({
            "Title":title,
            "Author":author
        })

        st.success("Book Added")

    st.subheader("Library Books")

    if st.session_state.books:

        df = pd.DataFrame(st.session_state.books)

        search = st.text_input("Search")

        if search:
            df = df[df["Title"].str.contains(search,case=False)]

        st.dataframe(df)

# STUDENTS
elif choice == "Students":

    name = st.text_input("Student Name")

    if st.button("Add Student"):

        st.session_state.students.append(name)

        st.success("Student Added")

    st.write(st.session_state.students)

# ISSUE BOOK
elif choice == "Issue Book":

    if st.session_state.books and st.session_state.students:

        book = st.selectbox("Book",[b["Title"] for b in st.session_state.books])
        student = st.selectbox("Student",st.session_state.students)

        due = st.date_input("Due Date")

        if st.button("Issue"):

            st.session_state.issued.append({
                "Book":book,
                "Student":student,
                "Due":due
            })

            st.success("Book Issued")

# RETURN BOOK
elif choice == "Return Book":

    if st.session_state.issued:

        df = pd.DataFrame(st.session_state.issued)

        book = st.selectbox("Select Book",df["Book"])

        if st.button("Return"):

            today = date.today()

            record = next(i for i in st.session_state.issued if i["Book"] == book)

            if today > record["Due"]:

                fine = (today-record["Due"]).days * 5

                st.warning(f"Late Return. Fine ₹{fine}")

            st.session_state.issued = [
                i for i in st.session_state.issued if i["Book"] != book
            ]

            st.success("Book Returned")
