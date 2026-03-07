import streamlit as st
from books import get_books
from borrow import issue_book

st.header("📚 Student Dashboard")

books = get_books()

search = st.text_input("Search Book")

for book in books:

    if search.lower() in book[1].lower():

        st.subheader(book[1])
        st.write("Author:",book[2])
        st.write("Genre:",book[3])

        if st.button(f"Issue {book[0]}"):
            issue_book(st.session_state.user_id,book[0])
            st.success("Book Issued!")
