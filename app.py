import streamlit as st
import json
import pandas as pd
import plotly.express as px
from auth import login,register
from recommender import recommend

st.set_page_config(page_title="Smart Library AI",layout="wide")

# LOAD BOOKS
with open("data/books.json") as f:
    books = json.load(f)["books"]

df = pd.DataFrame(books)

if "user" not in st.session_state:
    st.session_state.user=None
    st.session_state.role=None

# LOGIN PAGE
if not st.session_state.user:

    st.title("📚 Smart Library AI")

    tab1,tab2 = st.tabs(["Login","Register"])

    with tab1:

        u = st.text_input("Username")
        p = st.text_input("Password",type="password")

        if st.button("Login"):

            ok,role = login(u,p)

            if ok:

                st.session_state.user=u
                st.session_state.role=role
                st.rerun()

            else:
                st.error("Invalid login")

    with tab2:

        ru = st.text_input("New Username")
        rp = st.text_input("New Password",type="password")

        if st.button("Register"):

            if register(ru,rp):
                st.success("Account created")
            else:
                st.error("User exists")

else:

    st.sidebar.title("📚 Smart Library")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard","Search","AI Recommendation","Analytics"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.user=None
        st.rerun()

    if menu=="Dashboard":

        st.title("Library Dashboard")

        c1,c2,c3 = st.columns(3)

        c1.metric("Total Books",len(df))
        c2.metric("Authors",df.author.nunique())
        c3.metric("Genres",df.genre.nunique())

        st.dataframe(df.head(20))

    elif menu=="Search":

        q = st.text_input("Search Book")

        if q:

            res = df[df.title.str.contains(q,case=False)]

            st.dataframe(res)

    elif menu=="AI Recommendation":

        book = st.selectbox("Select Book",df.title)

        if st.button("Recommend"):

            rec = recommend(book,books)

            st.write("Recommended Books")

            for r in rec:
                st.write("-",r)

    elif menu=="Analytics":

        fig = px.histogram(df,x="genre")

        st.plotly_chart(fig)

        fig2 = px.pie(df,names="author")

        st.plotly_chart(fig2)
