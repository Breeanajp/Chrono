import streamlit as st
import sqlite3 as sqlite3
import hashlib
from loginPage import isLoggedIn
import requests
import streamlit.components.v1 as components

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
        #view calendar
        html_code = """
<style>
:root {
    --primary-clr: #b38add;
}
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Poppins" , sans-serif;
}
body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #e2e1dc;
}
.container{ 
    position: relative;
    width: 1200px;
    min-height: 850px;
    margin: 0 auto;
    padding: 5px;
    color: #fff;
    display: flex;
    border-radius: 10px;
    background-color: #373c4f;
}
.left {
    width: 90%;
    padding: 20px;
}
.calendar {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: space-between;
    color: #878895;
    border-radius: 5px;
    background-color: #fff;
}
.calendar::before,
.calendar::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 100%;
    width: 12px;
    height: 97%;
    border-radius: 0 5px 5px 0;
    background-color: #d3d5d6d7;
    transform: translateY(-50%);
}
.calendar::before {
    height: 94%;
    left: calc(100% + 12px);
    background-color: rgb(153, 153, 153);
}
.calendar .month{
    width: 100%;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 50px;
    font-size: 1.2rem;
    font-weight: 500;
    text-transform: capitalize;
}
.calendar .month .prev,
.calendar .month .next {
    cursor: pointer;
}
.calendar .month .prev:hover,
.calendar .month .next:hover {
    color: var(--primary-clr);
}
.calendar .weekdays {
    width: 100%;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    font-size: 1rem;
    font-weight: 500;
    text-transform: capitalize;
}
.calendar .weekdays div {
    width: 14.28%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.calendar .days {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    padding: 0 20px;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 20px;
}
.calendar .days .day {
    width: 14.28%;
    height: 90px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--primary-clr);
    border: 1px solid #f5f5f5;
}
.calendar .day:not(.prev-date , .next-date):hover {
    color : #fff;
    background-color: var(--primary-clr);
}
.calendar .days .prev-date,
.calendar .days .next-date {
    color: #b3b3b3
}
.calendar .days .active {
    position: relative;
    font-size: 2rem;
    color: #fff;
    background-color: var(--primary-clr);
}
.calendar .days .active::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    box-shadow: 0 0 10px 2px var(--primary-clr);
}
.calendar .days .today {
    font-size: 2rem;
}
.calendar .days .event {
    position: relative;
}
.calendar .days .event::after {
    content: ''; 
    position: absolute;
    bottom: 10%;
    left: 50%;
    width: 75%;
    height: 6px;
    border-radius: 30px;
    transform: translateX(-50%);
    background-color: var(--primary-clr);
}
.calendar .event:hover::after {
    background-color: #fff;
}
.calendar .active.event::after {
    background-color: #fff;
    bottom: 20%;
}
.calendar .active.event{
    padding-bottom: 10px;
}
.calendar .goto-today {
    width: 100%;
    height: 50px;   
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5px;
    padding: 0 20px;
    margin-bottom: 20px;
    color: var(--primary-clr);
}
 .calendar .goto-today .goto {
    display: flex;
    align-items: center;
    border-radius: 5px;
    overflow: hidden;
    border: 1px solid var(--primary-clr);
}
.calendar .goto-today .goto input {
    width: 100%;
    height: 30px;   
    outline: none;
    border: none;
    border-radius: 5px;
    padding: 0 20px;
    color: var(--primary-clr);
    border-radius: 5px;
}
.calendar .goto-today button {
    padding: 8px 10px;
    border: 1px solid var(--primary-clr);
    border-radius: 5px;
    background-color: transparent;
    cursor: pointer;
    color: var(--primary-clr);
}
.calendar .goto-today button:hover {
    color: #fff;
    background-color: var(--primary-clr);
}
.calendar .goto-today .goto button {
    border: none;
    border-left: 1px solid var(--primary-clr);
    border-radius: 0;
} 
</style>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="stylesheet" type="text/css" href="style.css"  />
    <link
      rel="stylesheet" 
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" 
      integrity="sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg==" 
      crossorigin="anonymous" 
      referrerpolicy="no-referrer" />
    <title>Calander</title>
  </head>  
  <body>
    <div class="container">
      <div class="left">
        <div class="calendar">
          <div class="month">
              <i class="fa fa-angle-left prev"></i>
                <div class="date">October 2024</div>
              <i class="fa fa-angle-right next"></i>
          </div>
          <div class="weekdays">
            <div>sun</div>
            <div>mon</div>
            <div>tue</div>
            <div>wed</div>
            <div>thur</div>
            <div>fri</div>
            <div>sat</div>
          </div>
          <div class="days">
            <div class="day prev-date">29</div>
            <div class="day prev-date">30</div>
            <div class="day">1</div>
            <div class="day">2</div>
            <div class="day">3</div>
            <div class="day event active">4</div>
            <div class="day today">5</div>
            <div class="day">6</div>
            <div class="day">7</div>
            <div class="day event">8</div>
            <div class="day">9</div>
            <div class="day">10</div>
            <div class="day">11</div>
            <div class="day">12</div>
            <div class="day">13</div>
            <div class="day">14</div>
            <div class="day">15</div>
            <div class="day">16</div>
            <div class="day">17</div>
            <div class="day">18</div>
            <div class="day">19</div>
            <div class="day">20</div>
            <div class="day event">21</div>
            <div class="day">22</div>
            <div class="day">23</div>
            <div class="day">24</div>
            <div class="day">25</div>
            <div class="day">26</div>
            <div class="day">27</div>
            <div class="day">28</div>
            <div class="day">29</div>
            <div class="day">30</div>
            <div class="day">31</div>
            <div class="day next-date">1</div>
            <div class="day next-date">2</div>
          </div>
          <div class="goto-today">
            <div class="goto">
              <input type="text" placeholder="mm/yyyy" class="date-input" >
              <button class="goto-btn">go</button>
            </div>
            <button class="today-btn">today</button>
          </div>
        </div>
      </div>
    </div>
    <script src="'script.js"></script>
  </body>
</html> 

<script>
    

</script>



"""



components.html(html_code, height=840, width=1000)










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

