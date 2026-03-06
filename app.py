import streamlit as st
import pandas as pd

st.title("Smart Library Management System")

if "books" not in st.session_state:
    st.session_state.books = []

menu = ["Add Book", "View Books"]

choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    title = st.text_input("Book Title")
    author = st.text_input("Author")

    if st.button("Add Book"):
        st.session_state.books.append({"Title": title, "Author": author})
        st.success("Book Added Successfully!")

elif choice == "View Books":
    st.subheader("Library Books")

    if len(st.session_state.books) > 0:
        df = pd.DataFrame(st.session_state.books)
        st.table(df)
    else:
        st.info("No books added yet.")
