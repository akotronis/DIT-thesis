from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from .. import services as app_services
from .. import utils as app_utils


Builder.load_file(app_utils.get_kivy_filepath(__file__))


class MySwitch(MDBoxLayout):
    disabled = BooleanProperty(False)
    label_text = StringProperty('Switch')
    switch_toggle_callback = ObjectProperty(lambda *args: None)


if __name__ == '__main__':
    app_services.configure_window()
    app_services.test_page(MySwitch)