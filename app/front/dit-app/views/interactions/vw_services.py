from datetime import datetime, timezone

import folium
from folium.plugins import Draw
import streamlit as st
from streamlit_folium import st_folium

import constants as cnst
import services as srv
import utils as utl
import pytz


@st.fragment
def create_zone(group_mng):
    st.session_state.pop('zone-mode', None)
    st.write(':material/flag: **Define new zones for the selected group** (*Single* zone per submition)')
    map = folium.Map(location=cnst.DEFAULT_MAP_CENTER, zoom_start=cnst.DEFAULT_MAP_ZOOM)
    Draw(draw_options={**cnst.COMMON_MAP_OPTIOS, 'polygon': {'allowIntersection': False}},
         edit_options={**cnst.COMMON_MAP_OPTIOS, 'poly': {'allowIntersection': False}}).add_to(map)
    folium.Marker(location=cnst.DEFAULT_MAP_CENTER, icon=utl.marker_icon(), tooltip=f'{cnst.DEFAULT_MAP_CENTER}').add_to(map)
    zones = st_folium(map, height=450, use_container_width=True)
    group_wdg, zone_wdg = st.columns(2)
    group = group_wdg.selectbox('Select a group', group_mng.groups, format_func=lambda x:x.name, index=None, placeholder='Select a group', label_visibility='collapsed')
    zone_name = zone_wdg.text_input('Enter zone name', placeholder='Enter zone name', label_visibility='collapsed')
    if st.button('Submit zone', use_container_width=True, type='primary'):
        st.session_state['zone-mode'] = 'create'
        if not group:
            utl.add_message_to_state('Please select a group')
        elif not zone_name:
            utl.add_message_to_state('Please enter a zone name')
        else:
            zone_objects = zones.get('all_drawings', []) or []
            if len(zone_objects) != 1:
                utl.add_message_to_state('Please submit a SINGLE zone')
            else:
                zone_data = srv.Zone.add_zone_properties(utl.nth(zone_objects), group, zone_name)
                code, data = srv.get_api().create_group_zone(zone_data)
                utl.add_response_message_to_state(code, data, f'Sucessfully submited zone "{zone_name}" for group "{group.name}"')
        st.rerun()


def add_zones_to_map(map, group):
    for zone in group.zones:
        folium.GeoJson(zone.data, style_function=lambda feature:{'weight': 2, 'fillOpacity': 0.5},
                       tooltip=folium.Tooltip(f'Name: {zone.name}')).add_to(map)


@st.fragment
def view_zones(group_mng):
    st.session_state.pop('zone-view', None)
    st.write(':material/activity_zone: **View /** :material/delete: **Delete existing zones for the selected group**')
    group = st.selectbox('Select a group', group_mng.groups, format_func=lambda x:x.name, index=None, placeholder='Select a group', label_visibility='collapsed')
    if group:
        st.session_state['zone-mode'] = 'view-delete'
        map_center = group.zones_center
        map = folium.Map(location=map_center, zoom_start=cnst.DEFAULT_MAP_ZOOM)
        folium.Marker(location=map_center, icon=utl.marker_icon(), tooltip=f'Center: {map_center}').add_to(map)
        add_zones_to_map(map, group)
        st_folium(map, height=450, use_container_width=True)
        if group.zones:
            selected_zones = st.multiselect('Select Zones', options=group.zones, format_func=lambda x:x.name, label_visibility='collapsed', placeholder='Select zones to delete')
            if st.button('Delete selected zones', use_container_width=True, type='primary'):
                if not selected_zones:
                    utl.add_message_to_state('Please select zones to delete')
                for zone in selected_zones:
                    code, data = srv.get_api().delete_zone(zone.id)
                    utl.add_response_message_to_state(code, data, f'Sucessfully deleted zone(s) for group "{group.name}"')
                st.rerun()
        

def add_zones_to_feature_group(feature_group, group):
    for zone in group.zones:
        feature_group.add_child(folium.GeoJson(
            zone.data,
            style_function=lambda feature: {'weight': 2, 'fillOpacity': 0.5},
            tooltip=folium.Tooltip(f'Name: {zone.name}')
        ))


def add_route_points_to_feature_group(feature_group, points):
    for point in points:
        feature_group.add_child(folium.Marker(
            location=point.coords,
            icon=utl.marker_icon(color=point.color),
            tooltip=str(point)
        ))


def add_edge_points_to_feature_group(feature_group, start_point, end_point):
    if start_point:
        coords = start_point[::-1]
        start, end = coords
        feature_group.add_child(folium.Marker(
            location=coords,
            icon=utl.marker_icon(color='green'),
            tooltip=f'START: ({start}, {end})'
        ))
    if end_point:
        coords = end_point[::-1]
        start, end = coords
        feature_group.add_child(folium.Marker(
            location=coords,
            icon=utl.marker_icon(color='red'),
            tooltip=f'END: ({start}, {end})'
        ))


@st.fragment(run_every=cnst.MONITORING_POLLING_INTERVAL)
def monitoring(monitor_from, group, user_ids, n_latest, path_points):
    map = folium.Map(location=group.zones_center, zoom_start=cnst.DEFAULT_MAP_ZOOM)
    # User featuregroup to avoid reloading the whole map and update certain portion instead
    fg = folium.FeatureGroup(name='routes')
    add_zones_to_feature_group(fg, group)
    user_ids = user_ids or [st.session_state.user_id]
    if path_points:
        if st.session_state['path-points-cnt'] > 0:
            index = len(path_points) - st.session_state['path-points-cnt']
            point = path_points[index]
            st.session_state['path-points-cnt'] -= 1
            location = srv.Point(*point[::-1], mock=True, user_id=utl.nth(user_ids))
            srv.get_api().create_location(location.data)
        add_edge_points_to_feature_group(fg, utl.nth(path_points), utl.nth(path_points, -1))
    locations_data = srv.get_locations(user_ids, monitor_from, n_latest, mock=bool(path_points))
    latest_points = [srv.Point.from_data(point) for point in locations_data]
    add_route_points_to_feature_group(fg, latest_points)
    st_folium(map, height=550, feature_group_to_add=fg, use_container_width=True)
        
