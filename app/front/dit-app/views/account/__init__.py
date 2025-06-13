from functools import partial

import streamlit as st

from constants import PAGES_DIR_NAME
from utils import resolve_view_path


resolve_view_path_partial = partial(resolve_view_path, section_init_path=__file__)

home_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/home.py'), title='Home', icon=':material/home:', default=True)
sign_in_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/sign_in.py'), title='Sign In', icon=':material/login:')
sign_out_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/sign_out.py'), title='Sign Out', icon=':material/logout:')