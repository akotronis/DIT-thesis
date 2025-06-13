import contextlib
import functools
import itertools
import json

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarText
from kivy.utils import platform
from kivymd.app import MDApp
from PIL import ImageGrab
from plyer import gps

import api
from . import utils as app_utils
from . import constants as app_constants


def configure_window():
    """
    Configure window size and position if app runs locally
    """
    try:
        # Check if app runs on mobile
        from android import permissions
    except:
        # If exception is raised the app runs locally
        with contextlib.suppress(Exception):
            try:
                resolution = ImageGrab.grab().size
            except:
                resolution = [2.5 * _ for _ in Window.system_size]
            WIDTH = 500
            Window.size = (WIDTH, 2408 / 1080 * WIDTH)
            # Window.top = 5
            # Window.left = 1200
            Window.left = resolution[0] - WIDTH


def test_page(page_cls):
    """
    Run a page separately for testing defined as `page_cls`
    """
    class TestApp(MDApp):
        def build(self):
            return page_cls()
        
    TestApp().run()


def process_error_messages(message):
    return str(message)


def make_dialog(message, type_='error'):
    icon_mapper = {
        'success':'check-circle-outline',
        'error':'close-circle-outline',
        'info':'information-outline',
    }
    MDDialog(
        MDDialogIcon(icon=icon_mapper[type_.lower()]),
        MDDialogSupportingText(text=message)
    ).open()


def make_snackbar(message, duration=4):
    MDSnackbar(
        MDSnackbarText(text=message),
        duration=duration,
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.5,
    ).open()


def get_outcome_and_display_message(status_code, response_data, success_msg=None):
    success = status_code < 400
    if success and success_msg:
        make_dialog(success_msg, 'success')
    elif not success:
        make_dialog(process_error_messages(response_data))
    return success


def handle_uninitialized_connection(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.server_url:
            make_dialog('Please initialize backend connection')
            return
        return func(self, *args, **kwargs)
    return wrapper


class AppElementsMixin:
    def set_app_elements(self):
        # Keep seion related data like user info
        self.session_state = {}
        # Backend server url
        self.server_url = None
        # Kivy clock managed eent for shering location
        self.share_location_event = None
        # Set to an infinite cycle iterator of the MOCK_PATH_POINTS when
        # to iterate over mock data
        self.mock_data_iterator = itertools.cycle(app_constants.MOCK_PATH_POINTS)
        # Current device location either from GPS or from mock data
        self.lat = self.lon = None
        self.permissions_accepted = False
        # UI elements
        self.nav_drawer = self.root.ids.nav_drawer
        self.user_icon = self.root.ids.toolbar.ids.user_icon
        self.share_location_switch = self.nav_drawer.ids.share_location_switch.ids.switch
        self.share_location_chips = self.nav_drawer.ids.share_location_chips
        self.gps_data_chip = self.share_location_chips.ids.gps_data
        self.gps_data_chip_text = self.share_location_chips.ids.gps.text
        self.mock_data_chip = self.share_location_chips.ids.mock_data
        self.mock_data_chip_text = self.share_location_chips.ids.mock.text
        self.nav_drawer_login = self.nav_drawer.ids.nav_drawer_login
        self.nav_drawer_sign_up = self.nav_drawer.ids.nav_drawer_sign_up
        self.nav_drawer_sign_out = self.nav_drawer.ids.nav_drawer_sign_out
        self.nav_drawer_groups_label = self.nav_drawer.ids.nav_drawer_groups_label
        self.nav_drawer_groups_list = self.nav_drawer.ids.nav_drawer_groups_list
        self.nav_drawer_hidable_divider = self.nav_drawer.ids.nav_drawer_hidable_divider

    @property
    def share_location(self):
        return all([
            not self.share_location_switch.disabled,
            self.share_location_switch.active
        ])
    
    @property
    def real_data_enabled(self):
        return all([
            self.share_location,
            not self.mock_data_chip.disabled,
            not self.mock_data_chip.active,
            self.permissions_accepted
        ])
    
    @property
    def mock_data_enabled(self):
        return all([
        self.share_location,
        not self.share_location_switch.disabled,
        self.mock_data_chip.active
    ])

class DisplayMixin:
    def toggle_navigation_items(self):
        if self.is_authenticated:
            app_utils.toggle_display_widget(self.nav_drawer_login)
            app_utils.toggle_display_widget(self.nav_drawer_sign_up)
            app_utils.toggle_display_widget(self.nav_drawer_sign_out, hide=False)
            app_utils.toggle_display_widget(self.nav_drawer_groups_label, hide=False)
            app_utils.toggle_display_widget(self.nav_drawer_groups_list, hide=False)
            app_utils.toggle_display_widget(self.nav_drawer_hidable_divider, hide=False)
        else:
            app_utils.toggle_display_widget(self.nav_drawer_login, hide=False)
            app_utils.toggle_display_widget(self.nav_drawer_sign_up, hide=False)
            app_utils.toggle_display_widget(self.nav_drawer_sign_out)
            app_utils.toggle_display_widget(self.nav_drawer_groups_label)
            app_utils.toggle_display_widget(self.nav_drawer_groups_list)
            app_utils.toggle_display_widget(self.nav_drawer_hidable_divider)

    def manage_navigation(self):
        self.nav_drawer.set_state("toggle")
        self.toggle_navigation_items()

    @staticmethod
    def toggle_password_visibility(instance, value):
        """
        Toggle password(s) input icon(s) and text visibility
        """
        instance.parent.password_input.password = not value
        instance.parent.password_icon.icon = f'eye{(not value) *"-off"}'
        if hasattr(instance.parent, 'confirm_password_input') and instance.parent.confirm_password_input:
            instance.parent.confirm_password_input.password = not value
        if hasattr(instance.parent, 'confirm_password_icon') and instance.parent.confirm_password_icon:
            instance.parent.confirm_password_icon.icon = f'eye{(not value) *"-off"}'
    
    def toggle_theme(self, instance, value):
        if value:
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
    
    def switch_screen(self, screen_name):
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = screen_name
        self.nav_drawer.set_state('close')


class AuthenticationMixin:
    DEAFULT_WELCOME_MESSAGE = 'Please login'
    welcome_message = StringProperty(DEAFULT_WELCOME_MESSAGE)

    @property
    def token(self):
        return self.session_state.get('user_info', {}).get('token')
    
    @property
    def email(self):
        return self.session_state.get('user_info', {}).get('email')
    
    @property
    def user_id(self):
        return self.session_state.get('user_info', {}).get('user_id')
    
    @property
    def is_authenticated(self):
        return bool(self.token)

    def make_api_headers(self):
        return {'Authorization': f'Token {token}'} if (token := self.token) else {}

    @property
    def api_srv(self):
        return api.DitService(self.server_url, self.make_api_headers())
    
    def add_user_info_to_state(self, token, email, id_):
        self.session_state['user_info'] = {'token': token, 'email': email, 'user_id':id_}

    def remove_user_info_from_state(self):
        self.session_state.pop('user_info', None)

    @handle_uninitialized_connection
    def authenticate_user(self, email, pswd):
        code, data = self.api_srv.authenticate_user(email, pswd)
        if get_outcome_and_display_message(code, data):
            app_utils.toggle_display_widget(self.user_icon, hide=False)
            self.share_location_switch.disabled = False
            self.add_user_info_to_state(data.get('token'), email, data.get('id'))
            self.welcome_message = self.get_welcome_message()
            self.switch_screen('home')

    @handle_uninitialized_connection
    def register_user(self, email, pswd, confirm_pswd):
        if pswd != confirm_pswd:
            make_dialog('Password fields dont\'t match')
            return
        code, data = self.api_srv.register_user(email, pswd)
        if get_outcome_and_display_message(code, data):
            app_utils.toggle_display_widget(self.user_icon, hide=False)
            self.share_location_switch.disabled = False
            self.add_user_info_to_state(data.get('token'), email, data.get('id'))
            self.welcome_message = self.get_welcome_message()
            self.switch_screen('home')

    def sign_out_user(self):
        app_utils.toggle_display_widget(self.user_icon)
        self.mock_data_chip.active = False
        self.share_location_switch.active = False
        self.share_location_switch.disabled = True
        self.remove_user_info_from_state()
        self.welcome_message = self.DEAFULT_WELCOME_MESSAGE
        self.switch_screen('home')

    def get_welcome_message(self):
        return f'Logged in user:\n{email}!' if (email := self.email) else self.DEAFULT_WELCOME_MESSAGE
    
    def user_popup(self):
        make_dialog(f'Logged in as: {self.email}', 'success')


class ConnectionMixin:
    def check_backend_request_completed(self, request, result):
        if request.resp_status:
            self.server_url = request.url
        self.pending_requests -= 1
        if self.pending_requests == 0:
            self.all_requests_done()

    def all_requests_done(self):
        self.root.ids.toolbar.ids.loading_button.active = False
        if not self.server_url:
            make_dialog(f'Backend server not accessible', 'error')
        else:
            make_dialog(f'Backend server on: {self.server_url}', 'success')

    def check_connection(self, timeout=5):
        """
        Check if backend server is reachable by trying all possible hosts.
        Manage toolbar icon
        """
        self.pending_requests = len(app_constants.BACKEND_HOSTS)
        self.root.ids.toolbar.ids.loading_button.active = True
        for host in app_constants.BACKEND_HOSTS:
            url = f'http://{host}:{app_constants.BACKEND_PORT}'
            UrlRequest(url,
                       on_success=self.check_backend_request_completed,
                       on_failure=self.check_backend_request_completed,
                       on_error=self.check_backend_request_completed,
                       timeout=timeout)


class LocationMixin:
    def post_location(self, lat, lon, mock=False):
        if self.server_url and self.user_id:
            location_type = 'REAL' if self.real_data_enabled else 'MOCK'
            Logger.info(f' POSTING "{location_type}" LOCATION '.center(100, '='))
            Logger.info(f'Latitude: {lat}, Longitude: {lon}, User ID: {self.user_id}')
            location_data = json.loads(app_constants.LOCATION_TEMPLATE.format(lat=lat, lon=lon, user_id=self.user_id, mock=f'{mock}'.lower()))
            Logger.info(f'Location: {location_data}')
            code, data = self.api_srv.create_location(location_data)
            return code, data
        Logger.info(f' NO SERVER URL OR LOGGED IN USER '.center(100, '='))
    
    def _share_location(self, dt):
        """
        Called on mock data clock scheduling
        """
        lon, lat = next(self.mock_data_iterator)
        self.post_location(lat, lon)

    @handle_uninitialized_connection
    def toggle_share_location_switch(self, instance, value):
        self.gps_data_chip.disabled = not value
        self.mock_data_chip.disabled = not value
        self.api_srv.patch_user_visibility(self.user_id, value)
        self.determine_share_location()

    def toggle_share_location_chip(self, instance, type):
        instance.active = not instance.active
        for chip in self.share_location_chips.children:
            if chip is not instance:
                chip.active = False
        self.determine_share_location()
    
    @handle_uninitialized_connection
    def determine_share_location(self):
        if not self.share_location:
            Logger.info(f' NOT SHARE LOCATION '.center(100, '='))
            self.stop_gps()
            self.stop_mock_data()
        elif self.real_data_enabled:
            Logger.info(f' REAL DATA ENABLED '.center(100, '='))
            self.stop_mock_data()
            self.start_gps()
        elif not self.mock_data_enabled:
            Logger.info(f' MOCK DATA DISABLED '.center(100, '='))
            self.stop_mock_data()
        elif self.mock_data_enabled:
            Logger.info(f' MOCK DATA ENABLED '.center(100, '='))
            self.stop_gps()
            self.share_location_event = Clock.schedule_interval(self._share_location, app_constants.SHARE_LOCATION_EVERY_SECS)

    def stop_mock_data(self):
        Logger.info(f' STOPING MOCK DATA '.center(100, '='))
        Clock.unschedule(self.share_location_event)

    def on_location(self, **kwargs):
        """
        Called on getting mobile gps location 
        """
        if not self.share_location:
            return
        Logger.info(f' GPS LOCATION '.center(100, '='))
        # Called when a new GPS location is received
        lat, lon = map(kwargs.get, ['lat', 'lon'])
        self.post_location(lat, lon)

    def _schedule_show_snackbar(self, *args):
        """
        Main-thread-only snackbar display
        """
        try:
            make_snackbar(*args)
        except Exception as e:
            Logger.error(f'Snackbar failed: {str(e)}')

    def on_status(self, stype, status):
        Logger.info(f' GPS STATUS'.center(100, '='))
        message = 'GPS location disabled.\nPlease enable for real data' if stype == 'provider-disabled' else 'GPS enabled!'
        Clock.schedule_once(lambda dt: self._schedule_show_snackbar(message))
    
    def _request_permissions_callback(self, permission, results):
        if all(results):
            Logger.info('App permissions ACCEPTED. Configuring GPS')
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            self.permissions_accepted = True
        else:
            Logger.info('App permissions REJECTED')

    def _request_permissions(self):
        if platform != 'android':
            return
        from android.permissions import Permission, request_permissions
        permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
        request_permissions(permissions, self._request_permissions_callback)

    def initialize_gps(self):
        Logger.info(f' INITIALIZING GPS '.center(100, '='))
        self._request_permissions()
            
    def start_gps(self):
        Logger.info(f' STARTING GPS '.center(100, '='))
        if self.permissions_accepted:
            Logger.info(f' Permissions accepted '.center(50, '='))
            gps.start(minTime=1000 * app_constants.SHARE_LOCATION_EVERY_SECS, minDistance=0)

    def stop_gps(self):
        Logger.info(f' STOPING GPS '.center(100, '='))
        if self.permissions_accepted:
            Logger.info(f' Permissions accepted '.center(50, '='))
            gps.stop()