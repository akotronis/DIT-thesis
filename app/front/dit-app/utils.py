from datetime import datetime
import itertools
from pathlib import Path
import random

import folium
import pytz
import streamlit as st

import constants as cnst


def resolve_view_path(section_view_file_path, section_init_path):
    entrypoint_path = Path.cwd()
    view_section_folder = Path(section_init_path).parent
    return (view_section_folder / section_view_file_path).relative_to(entrypoint_path)


def centered_text(text, tag='div', element=None):
    write_text_on = element or st
    write_text_on.markdown(f"<{tag} style='text-align: center;'>{text}</{tag}>", unsafe_allow_html=True)


def remove_state_messages(type_=None):
    if type_:
        st.session_state.pop(type_, None)
    else:
        for type_ in cnst.MessageIconMapper:
            st.session_state.pop(type_.name, None)


def display_state_messages():
    for type_ in cnst.MessageIconMapper:
        type_name = type_.name
        if message := st.session_state.get(type_name):
            getattr(st, type_name)(message, icon=type_.value)
    remove_state_messages()


def process_error_messages(message):
    return str(message)


def add_message_to_state(message, type_='error'):
    st.session_state[type_] = message


def add_response_message_to_state(status_code, response_data, success_msg=None):
    success = status_code < 400
    if success and success_msg:
        add_message_to_state(success_msg, 'success')
    elif not success:
        add_message_to_state(process_error_messages(response_data))
    return success


def centered_page_of(percent, obj=None):
    left = round((1 - percent) / 2, 2)
    right = 1 - percent - left
    obj = obj or st
    _, centered_page, _ = obj.columns([left, percent, right])
    return centered_page


def success_icon_message(message, obj=None):
    obj = obj or st
    obj.success(message, icon=cnst.MessageIconMapper.success.value)


def info_icon_message(message, obj=None):
    obj = obj or st
    obj.info(message, icon=cnst.MessageIconMapper.info.value)


def warning_icon_message(message, obj=None):
    obj = obj or st
    obj.warning(message, icon=cnst.MessageIconMapper.warning.value)


def error_icon_message(message, obj=None):
    obj = obj or st
    obj.error(message, icon=cnst.MessageIconMapper.error.value)


def marker_icon(color='blue'):
    return folium.Icon(color, icon='record')


def random_colors(k):
    colors_cnt = len(len(cnst.MARKER_COLORS))
    if k <= colors_cnt:
        return random.sample(cnst.MARKER_COLORS, k)
    diff = k - colors_cnt
    return cnst.MARKER_COLORS + random.sample(cnst.MARKER_COLORS, diff)


def format_timestamp(timestamp, from_str=True, timezone=False):
    if from_str:
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    format_str = '%A %d %b %Y %H:%M:%S'
    if timezone:
        format_str += ':%z'
    return timestamp.astimezone(pytz.timezone(cnst.TIMEZONE)).strftime(format_str)


def nth(iterable, n=0, default=None):
    """
    Return the nth item of an iterable or a default value
    if there is no nth element.
    Supports negative indexing as well.
    """
    if n < 0:
        iterable = iterable[::-1]
        n = - (n + 1)
    return next(itertools.islice(iterable, n, None), default)


def now_default_tz():
    now = datetime.now(tz=pytz.UTC)
    return now.astimezone(pytz.timezone(cnst.TIMEZONE))


if __name__ == '__main__':
    coords = (
        (23.6983667, 37.9623023),
        (23.6983667, 37.963302299999995),
        (23.699366700000002, 37.963302299999995),
        (23.699366700000002, 37.9623023),
        (23.6983667, 37.9623023)
    )