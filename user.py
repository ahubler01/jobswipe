import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import time

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///user_info.db')
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = 'student_info'
    user_type = Column(String)
    username = Column(String, primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    degree = Column(String)
    university = Column(String)
    graduation = Column(String)
    age = Column(Integer)

class Recruiter(Base):
    __tablename__ = 'recruiter_info'
    user_type = Column(String)
    username = Column(String, primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    company = Column(String)
    industry = Column(String)
    jobs = Column(String)


def sign_up():

    # Title
    st.title("User Profile Management")

    # Select user type
    user_type = st.selectbox("Select User Type", ["Student", "Recruiter"])

    # User inputs
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()


    # Specific inputs based on user type
    if user_type == "Student":
        degree = st.text_input("Degree")
        university = st.text_input("University")
        graduation = st.text_input("Expected graduation")
        age = st.number_input("Age", min_value=0, step=1)

        # Button to create student user
        if st.button("Sign Up as Student"):
            with st.spinner('Wait for it...'):
                time.sleep(2)
            # student_user = Student(user_type, username, email, hashed_password, degree, university, graduation, age)
            st.success(f"Student {username} created successfully")
            st.session_state['sign'] = True


    elif user_type == "Recruiter":
        company = st.text_input("Company")
        industry = st.text_input("Industry")
        jobs = st.number_input("Job Openings", min_value=0, step=1)

        # Button to create recruiter user
        if st.button("Sign Up as Recruiter"):
            with st.spinner('Wait for it...'):
                time.sleep(2)
            recruiter_user = Recruiter(user_type, username, email, hashed_password, company, industry, jobs)
            st.success(f"Recruiter {username} created successfully")
            st.session_state['sign'] = True

    return


