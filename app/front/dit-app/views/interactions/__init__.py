from functools import partial

import streamlit as st

from constants import PAGES_DIR_NAME
from utils import resolve_view_path


resolve_view_path_partial = partial(resolve_view_path, section_init_path=__file__)

chat_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/chat.py'), title='Chat', icon=':material/forum:')
monitoring_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/monitoring.py'), title='Monitoring', icon=':material/my_location:')
zones_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/zones.py'), title='Zones', icon=':material/activity_zone:')