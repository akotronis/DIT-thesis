import streamlit as st

import services as srv
import utils as utl


def validate_sign_in_form(email, pswd, confirm_pswd=None, sign_up=None):
    error_message = None
    login_form_incomplete = not sign_up and not all([email, pswd])
    signup_form_incomplete = sign_up and not all([email, pswd, confirm_pswd])
    if login_form_incomplete or signup_form_incomplete:
        error_message = 'Please provide all form fields'
    if sign_up and pswd != confirm_pswd:
        error_message = 'Password fields don\'t match'
    if error_message:
        utl.add_message_to_state(error_message)
    return not error_message


def add_user_info_to_state(token=None, email=None, id_=None):
    st.session_state.token = token
    st.session_state.email = email
    st.session_state.user_id = id_


def remove_user_info_from_state(all_=False):
    st.session_state.pop('frm-email', None)
    st.session_state.pop('frm-pswd', None)
    st.session_state.pop('frm-cnf-pswd', None)
    if all_:
        st.session_state.pop('email', None)
        st.session_state.pop('token', None)
        st.session_state.pop('user_id', None)


def sign_in_user(sign_up):
    email, pswd, confirm_pswd = map(st.session_state.get, ['frm-email', 'frm-pswd', 'frm-cnf-pswd'])
    remove_user_info_from_state()
    if validate_sign_in_form(email, pswd, confirm_pswd, sign_up):
        api_srv = srv.get_api()
        func = api_srv.register_user if sign_up else api_srv.authenticate_user
        code, data = func(email, pswd)
        if utl.add_response_message_to_state(code, data, f'Welcome {email}! 😍'):
            add_user_info_to_state(data.get('token'), email, data.get('id'))