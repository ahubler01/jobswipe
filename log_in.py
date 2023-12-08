import streamlit as st
from sqlalchemy import create_engine, Column, String, PickleType, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///user_info.db', echo=True)
Session = sessionmaker(bind=engine)

# User model
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

    def verify_password(self, input_password):
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
        return self.password == hashed_input_password

def authenticate(username, input_password):
    # Create a new session for database interaction
    with Session() as session:
        # Hash the input password
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()

        # Query the database for a user with the given username and password
        user = session.query(Student).filter_by(username=username, hashed_password=hashed_input_password).first()

        # Return True if user exists, False otherwise
        return user is not None

def show_login():
    st.title('Login Page')

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if authenticate(username, password):
            # Implement your post-login logic here
            # For example, set a flag in st.session_state to indicate login status
            st.session_state['authenticated'] = True
            st.session_state['user'] = username
            st.success("Login successful!")
            # Redirect to another page or change the view
        else:
            st.error("Authentication failed.")


