import folium
import streamlit as st

import constants as cnst
import services as srv
import utils as utl
from views.interactions import vw_services as vw_srv


group_mng = srv.GroupManager(srv.get_groups())

utl.display_state_messages()

page = utl.centered_page_of(.8)
with page:
    st.header('Zones Page', divider=True)
    create_col, view_del_col = page.columns(2)
    create_button = create_col.button('Create Zone', use_container_width=True)
    view_button = view_del_col.button('View / Delete Zones', use_container_width=True)
    if create_button or st.session_state.get('zone-mode') == 'create':
        vw_srv.create_zone(group_mng)
    if view_button or st.session_state.get('zone-mode') == 'view-delete':
        vw_srv.view_zones(group_mng)