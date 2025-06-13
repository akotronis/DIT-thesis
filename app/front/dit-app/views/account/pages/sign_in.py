import time

import streamlit as st

import constants as cnst
import utils as utl
from views.account import vw_services as vw_srv


utl.display_state_messages()

page = utl.centered_page_of(.4)
with page:
    sign_up = st.session_state.get('sign_up')
    utl.centered_text(f'Sign In to {cnst.APP_NAME}', 'h1')
    with st.form('sign_in'):
        st.markdown('#### Enter your credentials')
        email, password = st.text_input('Email', key='frm-email'), st.text_input('Password', type='password', key='frm-pswd')
        confirm_password = st.text_input('Confirm Password', type='password', key='frm-cnf-pswd') if sign_up else None
        button_name = 'Sign Up' if sign_up else 'Login'
        st.form_submit_button(button_name, use_container_width=True, type='primary', on_click=vw_srv.sign_in_user, args=[sign_up])
    with st.container():
        alternative_choice_text = 'Already have an account?' if sign_up else 'Don\'t have an account?'
        utl.centered_text(alternative_choice_text)
        st.write('')
        alternative_choice_button_name = 'Log In' if sign_up else 'Sign Up'
        if st.button(alternative_choice_button_name, use_container_width=True):
            st.session_state.sign_up = not sign_up
            st.rerun()