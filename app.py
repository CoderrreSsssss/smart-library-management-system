import streamlit as st
from database import create_tables
from books import add_book,get_books
from borrow import borrow_book
from reviews import add_review,get_reviews
from recommendation import recommend

create_tables()

st.title("📚 Smart AI Library")

menu = st.sidebar.selectbox(
"Menu",
["Add Book","Library","AI Recommendation"]
)

if menu=="Add Book":

    st.header("Add New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")

    if st.button("Add Book"):

        add_book(title,author,genre)

        st.success("Book Added")


elif menu=="Library":

    st.header("Public Library")

    books = get_books()

    for book in books:

        st.subheader(book[1])
        st.write("Author:",book[2])
        st.write("Genre:",book[3])

        if st.button(f"Borrow {book[0]}"):

            borrow_book(1,book[0])

            st.success("Book Borrowed")

        rating = st.slider(f"Rate {book[0]}",1,5)

        review = st.text_input("Write Review")

        if st.button(f"Submit Review {book[0]}"):

            add_review(book[0],rating,review)

        reviews = get_reviews(book[0])

        for r in reviews:

            st.write("⭐",r[0],"-",r[1])


elif menu=="AI Recommendation":

    st.header("🤖 AI Book Recommendation")

    rec = recommend()

    for r in rec:

        st.write("📖",r)
