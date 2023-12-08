import streamlit as st
from log_in import show_login
from user import sign_up
from home import JobSwipe
from job_list import JobList
from streamlit_option_menu import option_menu


# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'sign' not in st.session_state:
    st.session_state['sign'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

def main():
    if not st.session_state['authenticated']:

        if st.session_state['sign']:
            show_login()
        else:
            sign_up()

    else:

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
            options=['Job Match', 'Job List'],
            icons=['graph-up', 'clipboard-data'],
            menu_icon="Cast",
            default_index=0,
            orientation='horizontal', )

        if selected =="Job Match":
            jobswipe = JobSwipe()
            jobswipe.run()
        elif selected =="Job List":
            joblist = JobList()
            JobList.filter_job()



if __name__ == "__main__":
    main()
