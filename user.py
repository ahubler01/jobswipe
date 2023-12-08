import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, PickleType, distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import time

Base = declarative_base()
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
    industry = Column(PickleType)
    location = Column(PickleType)
    duration = Column(PickleType)
    type_of_work = Column(PickleType)
    company_size = Column(PickleType)
    experience_level = Column(PickleType)
    paid = Column(PickleType)
    skills = Column(PickleType)
    academic_credit = Column(PickleType)


class Recruiter(Base):
    __tablename__ = 'recruiter_info'
    user_type = Column(String)
    username = Column(String, primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    company = Column(String)
    industry = Column(String)
    jobs = Column(String)


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    company = Column(String)
    logo = Column(String)
    title = Column(String)
    industry = Column(String)
    location = Column(String)
    duration = Column(String)
    type_of_work = Column(String)
    company_size = Column(String)
    experience_level = Column(String)
    paid = Column(String)
    skills = Column(PickleType)
    keywords = Column(PickleType)
    academic_credit = Column(String)
    application_deadline = Column(String)

def get_unique_values():
    job_engine = create_engine('sqlite:///jobs.db')
    Job_Session = sessionmaker(bind=job_engine)
    job_session = Job_Session()

    unique_values = {}
    for column in Job.__table__.columns:
        column_name = column.name
        query = job_session.query(distinct(column)).all()
        unique_values[column_name] = [row[0] for row in query]

    job_session.close()

    return unique_values

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

        unique_values = get_unique_values()

        industry = st.multiselect('Which industry are you interested in?', unique_values["industry"])
        location = st.multiselect('What would be the best locations?', unique_values["location"])
        type_of_work = st.multiselect('What type of work are you interested in?', unique_values["type_of_work"])
        company_size = st.multiselect('What would be the optimal company size for you?', unique_values["company_size"])
        experience_level = st.multiselect('What is your experience?', unique_values["experience_level"])
        paid = st.multiselect('Do you want to get paid?', unique_values["paid"])
        skills = st.multiselect('From this list, what would be your skills?', [item for sublist in unique_values["skills"] for item in sublist])
        academic_credit = st.multiselect('Do you want to receive academic credit?', unique_values["academic_credit"])



        # Button to create student user
        if st.button("Sign Up as Student"):
            with st.spinner('Wait for it...'):

                student_user = Student(user_type=user_type, username=username, email=email, hashed_password=hashed_password, degree=degree, university=university, graduation=graduation, age=age, industry=industry, location=location, type_of_work=type_of_work, company_size=company_size, experience_level=experience_level, paid=paid, skills=skills, academic_credit=academic_credit)

                # Database setup
                engine = create_engine('sqlite:///user_info.db')
                Student.__table__.create(bind=engine, checkfirst=True)
                Session = sessionmaker(bind=engine)
                session = Session()
                session.add(student_user)
                session.commit()
                time.sleep(1)

            st.session_state['sign'] = True
            st.success(f"Student {username} created successfully")



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


