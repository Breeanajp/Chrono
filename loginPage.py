import streamlit as st
import sqlite3 as sqlite3
import hashlib

connection = sqlite3.connect('streamlitBase')
connect = connection.cursor()
isLoggedIn = False

username = st.text_input("Please enter a username")
password = st.text_input("Please choose a password")

text = ""


if st.button("Log in"):

    if username and password:  # Check if both fields are filled
        
        connect.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = connect.fetchone()
        
        if user:
            st.success(f"Welcome back, {username}! Your user ID is {user[0]}.")
            st.session_state.isLoggedIn = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password")
    else:
        st.error("Please fill in both fields before submitting.")
   

        


st.text(text)
