import streamlit as st
import pandas as pd
import json
import plotly.express as px
from auth import login,register

st.set_page_config(page_title="Smart Library",layout="wide")

# LOGIN SYSTEM
if "user" not in st.session_state:

    menu = ["Login","Register"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Login":
        login()
    else:
        register()

    st.stop()

st.title("📚 Smart Library Management System")

# LOAD DEFAULT BOOKS
if "books" not in st.session_state:

    with open("books.json") as f:
        data = json.load(f)

    st.session_state.books = data["books"]

menu = ["Dashboard","Books","Search"]

choice = st.sidebar.selectbox("Menu",menu)

# DASHBOARD
if choice == "Dashboard":

    total_books = len(st.session_state.books)

    col1,col2 = st.columns(2)

    col1.metric("Total Books",total_books)

    df = pd.DataFrame(st.session_state.books)

    chart = px.histogram(df,x="author",title="Books by Author")

    st.plotly_chart(chart,use_container_width=True)

# BOOK MANAGEMENT
elif choice == "Books":

    st.subheader("Add Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")

    if st.button("Add Book"):

        st.session_state.books.append({
            "title":title,
            "author":author
        })

        st.success("Book Added")

    st.subheader("Library Books")

    df = pd.DataFrame(st.session_state.books)

    st.dataframe(df,use_container_width=True)

# SEARCH BOOK
elif choice == "Search":

    query = st.text_input("Search Book")

    df = pd.DataFrame(st.session_state.books)

    if query:

        result = df[df["title"].str.contains(query,case=False)]

        st.dataframe(result)
