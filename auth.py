import streamlit as st
import json

def load_users():
    with open("users.json","r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json","w") as f:
        json.dump(users,f)

def login():

    st.subheader("Login")

    users = load_users()

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        if username in users and users[username]["password"] == password:

            st.session_state.user = username
            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")


def register():

    st.subheader("Register")

    users = load_users()

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password",type="password")

    if st.button("Register"):

        if new_user in users:
            st.error("User already exists")

        else:
            users[new_user] = {
                "password":new_pass,
                "role":"student"
            }

            save_users(users)

            st.success("User created")
