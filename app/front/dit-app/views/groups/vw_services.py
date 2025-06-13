import streamlit as st

import services as srv
import utils as utl


@st.dialog('CREATE group')
def create_group():
    st.markdown(f'Enter a name to ***CREATE*** a group')
    name = st.text_input('Group name:', placeholder='Group name')
    if st.button('Submit', use_container_width=True, type='primary'):
        code, data = srv.get_api().create_group(name)
        utl.add_response_message_to_state(code, data, f'Group "{name}" created successfully')
        st.rerun()


@st.dialog('Group Info')
def view_group(id_, name):
    st.markdown(f'**Name**: {name}')
    _, data = srv.get_api().get_group(id_)
    users = data.get('users', [])
    if users:
        st.write('**Members**:')
        for user in users:
            st.write(f'- ({user.get('id')}) - {user.get('email')}')


@st.dialog('EDIT group')
def edit_group(id_, name):
    updated_name = st.text_input('New group name:', placeholder=name)
    if st.button('Submit', use_container_width=True):
        code, data = srv.get_api().rename_group(id_, updated_name)
        utl.add_response_message_to_state(code, data, f'Group renamed successfully to "{updated_name}"')
        st.rerun()


@st.dialog('INVITE to group')
def invite_to_group(id_, name):
    invited_user_email = st.text_input('Invite user:', placeholder='example@email.com')
    if st.button('Invite', use_container_width=True):
        code, data = srv.get_api().invite_to_group(id_, invited_user_email)
        utl.add_response_message_to_state(code, data, f'User {invited_user_email} invited to group "{name}"')
        st.rerun()


@st.dialog('LEAVE group confirmation')
def leave_group(id_, name):
    st.markdown(f'Are you sure you want to ***LEAVE*** group **{name}**?')
    if st.button('Leave', use_container_width=True):
        code, data = srv.get_api().leave_group(id_)
        utl.add_response_message_to_state(code, data, f'Sucessfully left group "{name}"')
        st.rerun()


@st.dialog('DELETE group confirmation')
def delete_group(id_, name):
    st.markdown(f'Are you sure you want to ***DELETE*** group **{name}**?')
    if st.button('Delete', use_container_width=True, type='primary'):
        code, data = srv.get_api().leave_group(id_)
        utl.add_response_message_to_state(code, data, f'Sucessfully deleted group "{name}"')
        st.rerun()


@st.dialog('Invitation response')
def respond_to_invitation(id_, group_name):
    response = st.selectbox('Select Response', ['ACCEPT', 'REJECT'], index=None)
    submit = st.button('Submit Response', use_container_width=True, type='primary')
    if submit and response:
        status = f'{response}ED'
        code, data = srv.get_api().respond_to_invitation(id_, status)
        utl.add_response_message_to_state(code, data, f'Sucessfully {status} invitation to group "{group_name}"')
        st.rerun()