import streamlit as st
from sqlalchemy import create_engine, Column, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///user_info.db')
Session = sessionmaker(bind=engine)
session = Session()

# User model
class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)

    def verify_password(self, input_password):
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
        return self.password == hashed_input_password

def authenticate(username, input_password):
    user_query = select(User).where(User.username == username)
    user_result = session.execute(user_query).scalar_one_or_none()

    if user_result and user_result.verify_password(input_password):
        st.success(f'Welcome {user_result.username}!')
        st.session_state['authenticated'] = True
    else:
        st.error('Incorrect username or password')
        return False
    return True

def show_login():
    st.title('Login Page')

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
    if submit_button:
        if authenticate(username, password):
            st.experimental_rerun()
        else:
            st.error("Authentication failed.")
