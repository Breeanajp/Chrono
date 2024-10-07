import streamlit as st
import sqlite3


connection = sqlite3.connect('streamlitBase')
connect = connection.cursor()


connect.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, key TEXT)''')
connection.commit()
words = "Submit"
can = False

if 'show_text' not in st.session_state:
    st.session_state.show_text = True
if 'can_show_homepage' not in st.session_state:
    st.session_state.can_show_homepage = False


if st.session_state.show_text:

    username = st.text_input("Please enter a username")
    password = st.text_input("Please choose a password", type="password")

    if st.button(words):
        if username and password:
            try:
                connect.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                connection.commit()
                st.text("click again to exit login")
                st.success("User registered successfully!")
                st.session_state.show_text = False
                st.session_state.can_show_homepage = True
                can = True

                
                
                

            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose another.")
        
                    
        else:
            st.error("Please fill in both fields before submitting.")

if st.session_state.can_show_homepage:
    st.text("Thanks for registering, You can now login to your account")
