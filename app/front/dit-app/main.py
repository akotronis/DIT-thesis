from datetime import datetime, timezone
import random
import time
import streamlit as st

import services as srv

from views import account
from views import demos
from views import groups
from views import interactions


st.set_page_config(layout='wide')

is_authenticated = st.session_state.get('email')

auth_pages = [account.sign_out_page] if is_authenticated else [account.sign_in_page]
account_pages = [account.home_page] + auth_pages
group_pages = [groups.management_page, groups.invitations_page]
interaction_pages = [interactions.chat_page, interactions.zones_page, interactions.monitoring_page]
demo_pages = [demos.management_page]

srv.add_logo()

account_sectioned_pages = {'Account': account_pages}
group_sectioned_pages = {'Groups': group_pages}
interaction_sectioned_pages = {'Interactions': interaction_pages}
demo_sectioned_pages = {'Demos': demo_pages}

displayed_pages = account_sectioned_pages
if is_authenticated:# or 1 > 0:
    with st.sidebar:
        toggle_vsb_value = st.session_state.get('toggle-vsb', False)
        toggle_vsb_icon = ':material/visibility:' if toggle_vsb_value else ':material/visibility_off:'
        toggle_vsb_label = f'{toggle_vsb_icon} {"Visible" if toggle_vsb_value else "Invisible"}'
        st.write(f':material/visibility: Visibility')
        toggle_vsb = st.toggle(toggle_vsb_label, toggle_vsb_value, key='toggle-vsb')
        srv.get_api().patch_user_visibility(st.session_state.get('user_id'), toggle_vsb)
        st.divider()
        st.write(':material/notifications: Notifications')
        toggle_ntf_value = st.session_state.get('toggle-ntf')
        toggle_ntf_label = 'Active' if toggle_ntf_value else 'Inactive'
        if st.toggle(toggle_ntf_label, toggle_ntf_value, key='toggle-ntf'):
            srv.check_for_notifications()
    displayed_pages |= group_sectioned_pages | interaction_sectioned_pages | demo_sectioned_pages
pg = st.navigation(displayed_pages)

pg.run()