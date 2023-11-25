import streamlit as st
from log_in import show_login
from user import sign_up
from home import JobSwipe

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'sign' not in st.session_state:
    st.session_state['sign'] = False
def main():
    if st.session_state['authenticated']:

        jobswipe = JobSwipe()
        jobswipe.run()

    else:
        if st.session_state['sign']:
            show_login()
        else:
            sign_up()


if __name__ == "__main__":
    main()
