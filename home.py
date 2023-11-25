import streamlit as st
from PIL import Image
from sqlalchemy import create_engine, Column, String, Integer, select, PickleType, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from streamlit_option_menu import option_menu

Base = declarative_base()

class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    age_requirement = Column(Integer)
    major_requirement = Column(String)
    preferences = Column(PickleType)

# Database connection setup
engine = create_engine('sqlite:///jobs.db')
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
        if "results" not in st.session_state:
            st.session_state.results: list = []
        if "image" not in st.session_state:
            st.session_state.image: Image = None
        if "find_job" not in st.session_state:
            st.session_state.find_job: bool = False




    def run(self) -> None:
        """
        Entry point of the app. Calls other methods to show the sidebar, select images, create a task, and proceed to labeling.
        """
        st.set_page_config(
            page_title="Jobswipe",
            page_icon="👔",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.title("JOBSWIPE")

        # Display the Option menu
        selected = option_menu(
            menu_title=None,
            options=['Job Match', 'Job List', 'Profile'],
            icons=['graph-up', 'clipboard-data', 'people-fill'],
            menu_icon="Cast",
            default_index=0,
            orientation='horizontal', )

        # self.show_sidebar()

        if selected == "Job Match":
            self.label_images()

    def label_images(self) -> None:
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

        st.session_state.uploaded_files = ['apple.jpeg', '', 'google.jpeg', '', 'google.jpeg']

        uploaded_file = st.session_state.uploaded_files[st.session_state.counter]
        image = self.read_image(uploaded_file)
        st.session_state.image = image
        width, height = image.size
        new_width = int(width * st.session_state.target_height / height)
        image = image.resize((new_width, st.session_state.target_height))

        location = st.multiselect(
            'Location:',
            ['Madrid', 'Any', 'Astan', 'Rome'])
        job_type = st.multiselect(
            'Job Type:',
            ['Full-Time', 'On-Site', 'Remote'])

        col1,col2,col3 = st.columns(3)
        st.session_state.find_job = col2.button("Find your Job!")

        if st.session_state.find_job and location:
            jobs = self.filter_job(location, job_type)

            # st.markdown(jobs)
            if st.session_state.counter<len(jobs):

                position = jobs[st.session_state.counter].title
                location = jobs[st.session_state.counter].location
                age = jobs[st.session_state.counter].age_requirement
                requirement = jobs[st.session_state.counter].major_requirement
                preferences = jobs[st.session_state.counter].preferences

                st.header(position)
                st.image(image)

                columns = st.columns(4)
                with columns[0]:
                    st.button(
                        "❌", key=f'no_{st.session_state.counter}', on_click=self.save_results_no)
                with columns[3]:
                    st.button(
                        "✅", key=f'yes_{st.session_state.counter}', on_click=self.save_results(jobs))


                st.subheader(location)
                st.subheader(age)
                st.subheader(requirement)
                st.subheader(preferences)


                print(st.session_state.counter)

            else:
                st.session_state.counter = 0
                st.title("There are no more jobs available")


    def filter_job(self, location, job_type):

        jobs = session.query(Jobs).all()

        print(location)

        # Build a query to filter jobs based on location and job_type
        query = select(Jobs).where(
            or_(
                Jobs.location.in_(location),
                Jobs.preferences.in_(job_type)
            )
        )

        # Execute the query
        results = session.execute(query).scalars().all()

        print(f'the {results}')
        for job in results:
            print(job.preferences)


        return results

    def read_image(self, uploaded_file):
        image = Image.open(uploaded_file).convert("RGB")
        return image

    def increase_counter(self) -> None:
        """
        Increases the counter to move to the next image and displays it.
        """
        st.session_state.counter += 1

    def save_results(self, jobs) -> None:
        """
        Saves the result of the current image as 1 (yes) and moves to the next image.
        """

        st.session_state.results = jobs[st.session_state.counter]
        self.increase_counter()

jobswipe = JobSwipe()
jobswipe.run()

