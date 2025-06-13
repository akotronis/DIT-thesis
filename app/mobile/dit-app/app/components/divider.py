from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from .. import utils as app_utils


Builder.load_file(app_utils.get_kivy_filepath(__file__))


class MyDivider(MDBoxLayout):
    pass