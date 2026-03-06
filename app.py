import streamlit as st
import pandas as pd
from auth import login,register

st.set_page_config(page_title="Smart Library System")

if "user" not in st.session_state:

    menu = ["Login","Register"]

    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Login":
        login()

    else:
        register()

    st.stop()

st.title("📚 Smart Library Management System")

st.sidebar.write("Logged in as:",st.session_state.user)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

menu = ["Dashboard","Books","Students"]

choice = st.sidebar.selectbox("Menu",menu)

if "books" not in st.session_state:
    st.session_state.books = []

if choice == "Dashboard":

    st.metric("Total Books",len(st.session_state.books))

elif choice == "Books":

    title = st.text_input("Book Title")
    author = st.text_input("Author")

    if st.button("Add Book"):

        st.session_state.books.append({
            "Title":title,
            "Author":author
        })

        st.success("Book Added")

    if st.session_state.books:

        df = pd.DataFrame(st.session_state.books)

        st.dataframe(df)

elif choice == "Students":

    st.write("Student dashboard coming soon")
