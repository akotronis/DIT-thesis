from datetime import datetime
import random

import folium
import pytz
import streamlit as st

import constants as cnst
import services as srv
import utils as utl
from views.interactions import vw_services as vw_srv


group_mng = srv.GroupManager(srv.get_groups())

utl.display_state_messages()

page = utl.centered_page_of(.8)

def submit_callback():
    if not group:
        utl.add_message_to_state('Please select a group')
    if mode == 'Mock' and group and not group.zones:
        utl.add_message_to_state('Add a zone for the selected group')
    if 'error' not in st.session_state:
        st.session_state['mntr-expanded'] = False
    else:
        st.session_state['mntr-expanded'] = True

with page:
    submit = group = None
    st.header('Monitoring Page', divider=True)
    with st.expander('Configure monitoring settings', expanded=st.session_state.get('mntr-expanded', False)):
        if mode := st.pills('Monitor mode', ['Live', 'Mock']):
            time_col, rest_col = st.columns(2)
            now = utl.now_default_tz()
            from_date = time_col.date_input('Monitor start date', value=now.date())
            from_time = time_col.time_input('Monitor start time', value=st.session_state.get('mntr-time', now.time()), key='mntr-time')
            group = rest_col.selectbox('Select a group', group_mng.groups, format_func=lambda x:x.name, index=None)
            group_users = group.filter_visible_users() if group else []
            user_ids = []
            if mode == 'Live':
                users = rest_col.multiselect('Select Users', options=group_users, format_func=lambda x:x.email)
                user_ids = [user.id for user in users]
            n_latest = st.slider('Display n latest locations', min_value=1, max_value=10)
            monitor_from_local = pytz.timezone(cnst.TIMEZONE).localize(datetime.combine(from_date, from_time))
            monitor_from_utc = monitor_from_local.astimezone(pytz.utc).isoformat()
            submit = st.button('Submit', use_container_width=True, type='primary', on_click=submit_callback)
    if all([submit, mode, group]) and any([mode == 'Live', mode == 'Mock' and group.zones]):
        path_points = group.get_group_path_points() if mode == 'Mock' else []
        st.session_state['user-colors'] = {}
        st.session_state['path-points-cnt'] = len(path_points)
        vw_srv.monitoring(monitor_from_utc, group, user_ids, n_latest, path_points)