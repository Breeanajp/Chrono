import streamlit as st
import sqlite3 as sqlite3
import hashlib
from loginPage import isLoggedIn
import requests


st.session_state.bool1 = False


if 'token_saved' not in st.session_state:
    st.session_state.token_saved = False


connection = sqlite3.connect('streamlitBase')
connect = connection.cursor()

def homePageView():

    username = st.session_state.username

    connect.execute('''SELECT key FROM users WHERE username = ?''', (username,))
    testToken = connect.fetchone()
    
    if testToken[0] is None:



        
        #if the token has already been saved 

        #if st.session_state.token_saved:
        #    st.success("Token saved.")
        #    
#
##            testToken = connect.fetchone()
 #           #The users token is stored in userToken
 #           userToken = testToken[0]
            


     #   else:
            #the first thing we need to do is make the user enter their key and then write that to their name in the database
        st.text("Lets start off by connecting your canvas account. Please input your canvas token:")
            #put the users token into token
        token = ""
        token = st.text_input("Please enter your token")
        testToken = ""

            
        if st.button("Submit token"):

            if token and username:
                    testToken = ""

                    #connect to the sqlite database and put the users token in
                        
                    connect.execute('''UPDATE users SET key = ? WHERE username = ? ''', (token, username))
                    connection.commit()
                    connect.execute('''SELECT key FROM users WHERE username = ?''', (username,))
                    testToken = connect.fetchone()
                    if testToken and testToken[0] == token:
                        st.text("Click again to go home")
                        st.success(f"Token saved for {username}.")
                            
                        st.session_state.bool1 = True
                        st.session_state.token_saved = True
                    else:
                        st.error(f"Failed to save or retrieve the token for user {username}.")
    else:
        #create a list for course id's as well as names
        courseIDList = []
        courseNameList = []

        #define the link for the api
        apiLink = 'https://canvas.instructure.com/api/v1'

        #define headers for authentication
        headers = {
        'Authorization': f'Bearer {testToken[0]}'
        }

        #now generate the actual link to access the api endpoint we want, right here we are accesing courses
        #just append the endpointe "courses" to the root link
        link = f'{apiLink}/courses'

        #now print out all courses
        while link:
            #define the response using the requests tool
            response = requests.get(link, headers=headers)
            #check if the request receives an approriate response
            if response.status_code == 200:
                #take in the response in json form and put it into the var courses. 
                courses = response.json()
                #loop through each course in the response json var
                for course in courses:
                    #checking for name, because if we dont some courses that are random garbage without names or other defining characteristics will be included
                    if 'name' in course:
                        st.text(f"Course name: {course['name']}, Course ID: {course['id']}")
                        #append each courses id into the course id list. This makes them more easily accesable for other functions in the future
                        courseIDList.append(course['id'])
                        courseNameList.append(course['name'])
                        #check if there is a next page, otherwise end.
                    link = response.links.get('next', {}).get('url')
                    












#This is the code to retreive a specific users token
    #connect.execute('''SELECT key FROM users WHERE username = ?''', (username,))
    #testToken = connect.fetchone()



    



if 'isLoggedIn' not in st.session_state:
    st.session_state.isLoggedIn = False






#Check if the user is logged in, if they are display the homePage
if st.session_state.isLoggedIn and st.session_state.bool1 == False:
    homePageView()
else:
    st.text("Please log in to view home page.")

