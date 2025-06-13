import streamlit as st

import utils as utl
from views.account import vw_services as vw_srv


vw_srv.remove_user_info_from_state(all_=True)
utl.remove_state_messages()
st.rerun()