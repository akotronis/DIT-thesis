from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from .... import services as app_services
from .... import utils as app_utils


Builder.load_file(app_utils.get_kivy_filepath(__file__))


class SignUpScreen(MDScreen):
    pass


if __name__ == '__main__':
    app_services.configure_window()
    app_services.test_page(SignUpScreen)