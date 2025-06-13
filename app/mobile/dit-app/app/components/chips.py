from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from .. import services as app_services
from .. import utils as app_utils


Builder.load_file(app_utils.get_kivy_filepath(__file__))


class MyChips(MDBoxLayout):
    """"""