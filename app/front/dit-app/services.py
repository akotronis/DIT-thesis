from datetime import datetime
import functools
import random

from geopy.distance import geodesic
import numpy as np
import requests
from shapely.geometry import Polygon
import streamlit as st

import api
import constants as cnst
import utils as utl


class Point:
    def __init__(self, lat, lon, mock=False, user_id=None):
        self.lat = lat
        self.lon = lon
        self.mock = mock
        self.user_id = user_id
        self.email = None
        self.created_at = None

    @property
    @functools.lru_cache
    def data(self):
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    self.lon,
                    self.lat
                ]
            },
            'properties': {
                'mock': self.mock,
                'user': self.user_id
            }
        }
    
    @property
    @functools.lru_cache
    def coords(self):
        return self.lat, self.lon
    
    @classmethod
    def from_data(cls, data):
        lon, lat = data['geometry']['coordinates']
        mock = bool(data['properties']['mock'])
        user_id = data['properties']['user']
        obj = cls(lat, lon, mock, user_id)
        obj.email = data['properties']['email']
        obj.created_at = data['properties']['created_at']
        return obj
    
    @property
    def color(self):
        user_colors = st.session_state.get('user-colors', {})
        if self.user_id in user_colors:
            return user_colors[self.user_id]
        excluded_colors = ['red', 'green']
        used_colors = list(user_colors.values())
        available_colors = [clr for clr in cnst.MARKER_COLORS if clr not in excluded_colors + used_colors]
        user_color = random.choice(available_colors or cnst.MARKER_COLORS)
        user_colors[self.user_id] = user_color
        return user_color
    

    def __str__(self):
        return f'({self.lat}, {self.lon})</br>{self.email}</br>{self.created_at}'


class Zone:
    def __init__(self, data):
        self.data = data
        self.id = self.data.get('id')
        self.name = self.data.get('properties', {}).get('name')
        self.created_at = self.data.get('properties', {}).get('created_at')
        self.group_id = self.data.get('properties', {}).get('group_id')
        coordinates = utl.nth(self.data.get('geometry', {}).get('coordinates', []), default=[])
        # Change to lat, lon required by map from lon, lat sent from backend
        self.coordinates = [coord[::-1] for coord in coordinates]
    
    @property
    @functools.lru_cache
    def center(self):
        centroid = Polygon(self.coordinates).centroid
        return centroid.x, centroid.y
    
    @classmethod
    def add_zone_properties(cls, zone_data, group, zone_name):
        properties = zone_data.setdefault('properties', {})
        properties['name'] = zone_name
        properties['group'] = group.id
        return zone_data


class User:
    def __init__(self, data):
        self.data = data
        self.id = self.data.get('id')
        self.email = self.data.get('email')
        self.visible = bool(self.data.get('visible'))


class Group:
    def __init__(self, data):
        self.data = data
        self.id = self.data.get('id')
        self.name = self.data.get('name')
        self.users = [User(user_data) for user_data in self.data.get('users', [])]
        self.zones = [Zone(zone_data) for zone_data in self.data.get('zones', {}).get('features', [])]

    def filter_visible_users(self, visible=True):
        return [u for u in self.users if u.visible == visible]
    
    def get_zone_ids_from_names(self, zone_names):
        return [zone.id for zone in self.zones if zone.name in zone_names]
    
    def get_user_by_email(self, email):
        return utl.nth([u for u in self.users if u.email == email])
    
    @property
    @functools.lru_cache
    def zone_names(self):
        return [zone.name for zone in self.zones]
    
    @property
    @functools.lru_cache
    def zones_center(self):
        if len(self.zones) == 1:
            return utl.nth(self.zones).center
        elif not self.zones:
            return cnst.DEFAULT_MAP_CENTER
        centroid = Polygon([zone.center for zone in self.zones]).centroid
        return centroid.x, centroid.y
    
    def get_group_path_points(self):
        # Change to lon, lat required by backend from lat, lon required by the map
        start_point = cnst.DEFAULT_MAP_CENTER[::-1]
        end_point = random.choice(self.zones).center[::-1]
        path_points = get_path_points(start_point, end_point)
        all_path_points = [start_point] + path_points + [end_point]
        return all_path_points


def get_path_points(start, end):
    """
    Fetch route between two points.
    E.g.
    start_point = (23.7275, 37.9838) lon, lat
    end_point = (23.7310, 37.9870) lon, lat
    """
    start_coords = f'{start[0]},{start[1]}'
    end_coords = f'{end[0]},{end[1]}'
    url = f'{cnst.OSRM_API}/{start_coords};{end_coords}'
    response = requests.get(url, params={'overview':'full', 'geometries':'geojson'})
    if response.status_code == 200:
        data = response.json()
        return data['routes'][0]['geometry']['coordinates']
    else:
        raise Exception(f'Error fetching route: {response.status_code}')
    

class GroupManager:
    def __init__(self, data):
        self.data = data
        self.groups = [Group(group_data) for group_data in self.data]

    @property
    @functools.lru_cache
    def group_names(self):
        return [gr.name for gr in self.groups]

    def get_group_from_name(self, name):
        return next(iter([gr for gr in self.groups if gr.name == name]), None)


def add_logo():
    st.logo(cnst.LOGO_PATH_EXPANDED, icon_image=cnst.LOGO_PATH_COLLAPSED)


def notification_text(notification):
    email, zone, group = map(notification.get, ['email', 'zone_name', 'group_name'])
    timestamp = utl.format_timestamp(notification.get('created_at'))
    ntf_type = notification.get('type')
    if ntf_type == 'ENTRANCE':
        return f'[{timestamp}]\n"{email}" entered zone "{zone}" of group "{group}"'
    elif ntf_type == 'EXIT':
        return f'[{timestamp}]\n"{email}" exited zone "{zone}" of group "{group}"'
    return f'[{timestamp}]\n"{email}" sent a message in group "{group}"'


@st.dialog('New notifications', width='large')
def notification_button_callback(notifications):
    with st.container(height=300, border=False):
        for i, ntf in enumerate(notifications, 1):
            row = st.container(border=True).columns([.6, .4], vertical_alignment='center')
            row[0].text(notification_text(ntf))
    ntf_ids = [ntf.get('id') for ntf in notifications]
    get_api().patch_notifications(ntf_ids, seen=True)


@st.fragment(run_every=cnst.NOTIFICATION_POLLING_INTERVAL)
def check_for_notifications():
    notifications = get_notifications(seen=False)
    if notifications:
        st.button('New notification(s)!', use_container_width=True,
                    type='primary', icon=':material/notifications_active:',
                    on_click=notification_button_callback, args=[notifications])


def remove_notiication_info_from_state():
    st.session_state.pop('latest-ntf-id', None)


def make_api_headers():
    token = st.session_state.get('token')
    return {'Authorization': f'Token {token}'} if token else {}


def get_api():
    return api.DitService(headers=make_api_headers())


def get_groups():
    code, data = get_api().get_groups()
    utl.add_response_message_to_state(code, data)
    return data.get('results', []) or []


def get_locations(user_ids, monitor_from, n_latest, mock=True, visible=True):
    _, data = get_api().get_locations(user_ids, monitor_from, n_latest, mock=mock, visible=visible)
    return data.get('features', []) or []


def get_notifications(seen):
    _, data = get_api().get_notifications(seen)
    result = data.get('results', []) or []
    return result


def interpolate_route(route, num_points):
    """
    Interpolate a fixed number of points along the route.
    """
    
    if len(route) == 2:
        return route
    # Convert route to lat/lon tuples
    route_coords = [(lat, lon) for lon, lat in route]
    
    # Calculate cumulative distances along the route
    distances = [0]  # Start with zero distance
    for i in range(1, len(route_coords)):
        dist = geodesic(route_coords[i-1], route_coords[i]).meters
        distances.append(distances[-1] + dist)
    
    # Total route distance
    total_distance = distances[-1]
    
    # Generate evenly spaced distances
    target_distances = np.linspace(0, total_distance, num_points)
    
    # Interpolate points
    interpolated_points = []
    for target in target_distances:
        for i in range(1, len(distances)):
            if distances[i-1] <= target <= distances[i]:
                # Interpolate between points
                fraction = (target - distances[i-1]) / (distances[i] - distances[i-1])
                lat = route_coords[i-1][0] + fraction * (route_coords[i][0] - route_coords[i-1][0])
                lon = route_coords[i-1][1] + fraction * (route_coords[i][1] - route_coords[i-1][1])
                interpolated_points.append((float(lat), float(lon)))
                break
    return interpolated_points



if __name__ == '__main__':
    start = cnst.DEFAULT_MAP_CENTER
    x, y = cnst.DEFAULT_MAP_CENTER
    end = x - 5 * cnst.DEFAULT_OFFSET, y - 5 * cnst.DEFAULT_OFFSET

    start = (37.9583023, 23.6943667)[::-1]
    end = (37.9647023, 23.7007667)[::-1]


    points = get_path_points(start, end, 5)
    print(points)