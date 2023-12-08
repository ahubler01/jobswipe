import streamlit as st
from PIL import Image
from sqlalchemy import create_engine, Column, String, Integer, select, PickleType, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
import pandas as pd

Base = declarative_base()

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
    # score = Column(Integer)

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


# Database connection setup
engine = create_engine('sqlite:///user_info.db')
Session = sessionmaker(bind=engine)
session = Session()

class JobSwipe():
    def __init__(self):
        if "target_height" not in st.session_state:
            st.session_state.target_height: int = 500
        if "counter" not in st.session_state:
            st.session_state.counter: int = 0
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files: List = []
        if "label" not in st.session_state:
            st.session_state.label: str = ""
        if "match" not in st.session_state:
            st.session_state.match: list = []
        if "image" not in st.session_state:
            st.session_state.image: Image = None
        if "find_job_button" not in st.session_state:
            st.session_state.find_job_button: int = 0

    def run(self) -> None:
        """
        Displays the images and buttons for labeling.
        """
        # empty placeholders
        self.img_placeholder = st.empty()
        self.buttons_placeholder = st.empty()

        self.display_image()

    def display_image(self) -> None:
        """
        Displays the current image and buttons for labeling.
        """
        columns = st.columns(3)
        very_important = columns[0].multiselect(
            'Very Important Criterias:',
            [   "industry",
                "location",
                "duration",
                "type_of_work",
                "company_size",
                "experience_level",
                "paid",
                "skills",
                "keywords",
                "academic_credit",
            ])
        important = columns[1].multiselect(
            'Important Criterias:',
            [   "industry",
                "location",
                "duration",
                "type_of_work",
                "company_size",
                "experience_level",
                "paid",
                "skills",
                "academic_credit",
            ])
        less_important = columns[2].multiselect(
            'Less Important Criterias:',
            [   "industry",
                "location",
                "duration",
                "type_of_work",
                "company_size",
                "experience_level",
                "paid",
                "skills",
                "academic_credit",
            ])

        preference_importance = {
            'very_important': very_important,
            'important': important,
            'less_important': less_important,
        }

        st.session_state.find_job = st.button("Find your Job!", on_click = lambda: self.bool_counter('find_job_button'))

        if st.session_state.find_job_button:
            self.scoring(preference_importance)
            jobs = session.query(Job).all()

            st.markdown(len(jobs))
            if st.session_state.counter<len(jobs):

                position = jobs[st.session_state.counter].title
                company = jobs[st.session_state.counter].company  # Added company name
                logo = jobs[st.session_state.counter].logo
                location = jobs[st.session_state.counter].location
                type_of_work = jobs[st.session_state.counter].type_of_work
                duration = jobs[st.session_state.counter].duration
                experience_level = jobs[st.session_state.counter].experience_level
                skills = ', '.join(jobs[st.session_state.counter].skills)  # Assuming skills is a list
                paid = jobs[st.session_state.counter].paid
                company_size = jobs[st.session_state.counter].company_size
                academic_credit = jobs[st.session_state.counter].academic_credit
                industry = jobs[st.session_state.counter].industry


                with st.columns(3)[1]:
                    st.header(position)
                    st.image(logo)
                    st.markdown(company)  # Display the company name
                    st.markdown(location)
                    st.markdown(type_of_work + " | " + duration)  # Combining type of work and duration
                    st.markdown(f"**Experience Level:** {experience_level}")
                    st.markdown(f"**Skills Required:** {skills}")
                    st.markdown(f"**Paid/Unpaid:** {paid}")
                    st.markdown(f"**Company Size:** {company_size}")
                    st.markdown(f"**Industry:** {industry}")
                    if academic_credit:
                        st.markdown(f"**Academic Credit:** {academic_credit}")

                columns = st.columns(3)
                with columns[1]:
                    st.button(
                        "❌", key=f'no_{st.session_state.counter}', on_click=lambda: self.increase_int_counter('counter'))
                with columns[2]:
                    st.button("✅", key=f'yes_{st.session_state.counter}', on_click=lambda: self.save_results(jobs, 'counter'))



                if st.checkbox('Want to see your match?'):
                    if st.session_state.match:
                        with engine.connect() as conn:
                            query = select([Job]).where(Job.id.in_(st.session_state.match))
                            data = pd.read_sql(query, conn)
                            st.dataframe(data)
                    else:
                        st.markdown("***No match for the moment, keep hope!***")

            else:
                st.session_state.counter = 0
                st.title("There are no more jobs available")

    def selection_sort(self, arr, col):
        n = len(arr)

        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if getattr(arr[j], col) > getattr(arr[min_index], col):
                    min_index = j

            # Swap the objects in the list
            arr[i], arr[min_index] = arr[min_index], arr[i]

            # Update the 'order' attribute to reflect the new order
            arr[i].order, arr[min_index].order = i, min_index

        # Commit the changes to the database
        session.commit()

        return arr

    def scoring(self, preference_importance):
        def calculate_match_score(user, position, preference_importance, weights):
            total_score = 0

            for importance_level, preferences in preference_importance.items():
                for preference in preferences:
                    user_value = getattr(user, preference)
                    position_value = getattr(position, preference, None)

                    if isinstance(user_value, list):
                        if isinstance(position_value, list):
                            # Calculate matching score for lists
                            common_elements = set(user_value).intersection(position_value)
                            if common_elements:
                                total_score += (weights[importance_level] / len(user_value)) * len(common_elements)
                        elif position_value in user_value:
                            # Add full weight if the position_value is in the user_value list
                            total_score += weights[importance_level]
                    elif user_value == position_value:
                        # Add the weight if the values match
                        total_score += weights[importance_level]

            return total_score

        weights = {
            'very_important': 3,
            'important': 2,
            'less_important': 1
        }
        # Example usage within an SQLAlchemy session
        with Session() as session:
            # Assuming you're calculating the score for a specific user
            user = session.query(Student).filter_by(username=st.session_state['user']).first()

            if user:
                # Reset the score for each job
                for position in session.query(Job).all():
                    position.score = 0

                positions = session.query(Job).all()
                for position in positions:
                    position.score = calculate_match_score(user, position, preference_importance, weights)
                    # print(position.score)
                self.selection_sort(positions, 'score')
                session.commit()

    def read_image(self, uploaded_file):
        image = Image.open(uploaded_file).convert("RGB")
        return image

    # def increase_counter(self) -> None:
    #     """
    #     Increases the counter to move to the next image and displays it.
    #     """
    #     st.session_state.counter += 1

    def increase_int_counter(self, session_state_key: str) -> None:
        """
        Increases the specified counter in the session state to move to the next image and displays it.
        :param session_state_key: The key of the session state variable to be incremented.
        """
        if session_state_key in st.session_state:
            st.session_state[session_state_key] += 1
        else:
            st.error(f"Session state key '{session_state_key}' does not exist.")

    def bool_counter(self, session_state_key: str) -> None:
        """
        Increases the specified counter in the session state to move to the next image and displays it.
        :param session_state_key: The key of the session state variable to be incremented.
        """
        if session_state_key in st.session_state:
            st.session_state[session_state_key] = not st.session_state[session_state_key]
        else:
            st.error(f"Session state key '{session_state_key}' does not exist.")

    def save_results(self, jobs, session_state_key) -> None:
        """
        Saves the result of the current image as 1 (yes) and moves to the next image.
        """

        st.session_state.match.append(st.session_state.counter+1)
        self.increase_int_counter(session_state_key)

