import json
import os

import app.constants as app_constants


def get_kivy_filepath(py_file):
    ext = 'kv'
    path, _ = os.path.splitext(py_file)
    return f'{path}.{ext}'


def join_with_pyfile_dir(py_file, file):
    file_dir, _ = os.path.split(py_file)
    return os.path.join(file_dir, file)


def toggle_display_widget(wid, hide=True):
    # If widget has saved attributes, restore or save them as needed
    if hasattr(wid, 'saved_attrs'):
        if not hide:
            # Show the widget: restore its original attributes
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled, wid.theme_text_color, wid.text_color = wid.saved_attrs
            # Remove saved attributes after restoring them
            del wid.saved_attrs
    elif hide:
        # Save the current attributes before hiding the widget
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled, getattr(wid, 'theme_text_color', None), getattr(wid, 'text_color', None)
        # Hide the widget: set its attributes to make it invisible
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


def user_location_data(lat, lon, user_id):
    return json.loads(app_constants.LOCATION_TEMPLATE.format(lat=lat, lon=lon, user_id=user_id))