from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.progressindicator import MDCircularProgressIndicator

from .. import services as app_services
from .. import utils as app_utils


Builder.load_file(app_utils.get_kivy_filepath(__file__))


class MyLoadingIndicator(MDCircularProgressIndicator):
    active = BooleanProperty(False)


class MyTopToolBar(MDTopAppBar):
    pass


if __name__ == '__main__':
    app_services.configure_window()
    app_services.test_page(MyTopToolBar)