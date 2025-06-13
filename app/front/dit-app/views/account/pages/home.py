import streamlit as st

import constants as cnst
import utils as utl


utl.display_state_messages()

utl.centered_text(f'Welcome to {cnst.APP_NAME}', 'h1')
if email := st.session_state.get('email'):
    st.markdown(f'## Logged in as: {email}')
else:
    st.markdown(f'## Please Sign In')