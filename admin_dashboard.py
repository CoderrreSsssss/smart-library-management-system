import streamlit as st
from books import add_book,delete_book,get_books
from borrow import get_all_issued

st.header("🛠 Admin Panel")

title = st.text_input("Book Title")
author = st.text_input("Author")
genre = st.text_input("Genre")

if st.button("Add Book"):
    add_book(title,author,genre)
    st.success("Book Added")

books = get_books()

for book in books:

    st.write(book)

    if st.button(f"Delete {book[0]}"):
        delete_book(book[0])

st.subheader("Issued Books")

issued = get_all_issued()

for i in issued:
    st.write(i)
