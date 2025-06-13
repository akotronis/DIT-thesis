import streamlit as st

import services as srv
import utils as utl
from views.groups import vw_services as vw_srv


utl.display_state_messages()

page = utl.centered_page_of(.8)
with page:
    st.header(f'My Groups', divider=True)
    groups = srv.get_groups()
    st.button('Create a group', use_container_width=True, icon=':material/add:', type='primary', on_click=vw_srv.create_group, key='group-create')
    with st.container(height=500, border=False):
        for group_obj in groups:
            group_id, group_name = group_obj['id'], group_obj['name']
            extra_kwargs = {'id_':group_id, 'name': group_name}
            common_button_kwargs = {'use_container_width': True, 'kwargs': extra_kwargs}
            row = st.container(border=True).columns([.5, .1, .1, .1, .1, .1], vertical_alignment='center')
            row[0].write(f'({group_id}) - {group_name}')
            row[1].button('', help='Group info', icon=':material/info:', **common_button_kwargs, on_click=vw_srv.view_group, key=f'{group_id}-info')
            row[2].button('', help='Edit group', icon=':material/edit:', **common_button_kwargs, on_click=vw_srv.edit_group, key=f'{group_id}-edit')
            row[3].button('', help='Invite user to group', icon=':material/outgoing_mail:', **common_button_kwargs, on_click=vw_srv.invite_to_group, key=f'{group_id}-invite')
            row[4].button('', help='Leave group', icon=':material/move_item:', **common_button_kwargs, on_click=vw_srv.leave_group, key=f'{group_id}-leave')
            row[5].button('', help='Delete group', icon=':material/delete:', type='primary', **common_button_kwargs, on_click=vw_srv.delete_group, key=f'{group_id}-delete')