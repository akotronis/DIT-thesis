from functools import partial

import streamlit as st

from constants import PAGES_DIR_NAME
from utils import resolve_view_path


resolve_view_path_partial = partial(resolve_view_path, section_init_path=__file__)

management_page = st.Page(resolve_view_path_partial(f'{PAGES_DIR_NAME}/mock.py'), title='Mock', icon=':material/data_object:')