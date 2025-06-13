from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.screen import MDScreen
from kivymd.font_definitions import theme_font_styles
from kivy.logger import Logger

import app.services as app_services
import app.utils as app_utils

### Import pages/components
from app.components.chips import MyChips
from app.components.divider import MyDivider
from app.components.switch import MySwitch
from app.components.toolbar import MyTopToolBar
from app.components.navigation import MyNavigationDrawer
from app.views.account.pages.home import HomeScreen
from app.views.account.pages.login import LogInScreen
from app.views.account.pages.sign_up import SignUpScreen
from app.views.groups.pages.management import ManagementScreen
from app.views.groups.pages.invitations import InvitationsScreen

############### KIVY RELOADER ###############
# import trio
# from kivy_reloader.app import App as KRApp
#############################################

class MainScreen(MDScreen):
    pass


class MainApp(
    app_services.AppElementsMixin,
    app_services.DisplayMixin,
    app_services.AuthenticationMixin,
    app_services.ConnectionMixin,
    app_services.LocationMixin,
    ############### KIVY RELOADER ###############
    # KRApp,
    #############################################
    MDApp
):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        return MainScreen()
    
    def on_start(self):
        self.set_app_elements()
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 1
        app_utils.toggle_display_widget(self.user_icon)
        # self.share_location_switch.disabled = True
        self.gps_data_chip.active = True
        self.gps_data_chip.disabled = True
        self.mock_data_chip.disabled = True
        # Request GPS permissions and start updates
        self.initialize_gps()

    def on_pause(self):
        """
        Pause GPS when app is paused
        """
        self.stop_gps()
        return True

    def on_resume(self):
        """
        Resume GPS when app returns
        """
        self.determine_share_location()

Logger.info(f' INITIALIZING ****** '.center(100, '='))
app_services.configure_window()
MainApp().run()
############### KIVY RELOADER ###############
# trio.run(MainApp().async_run, 'trio')
#############################################