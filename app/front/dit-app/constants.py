from enum import Enum
import os


NOTIFICATION_POLLING_INTERVAL = 1
MONITORING_POLLING_INTERVAL = 1


LOGO_PATH_EXPANDED = 'images/horizontal_blue.png'
LOGO_PATH_COLLAPSED = 'images/icon_blue.png'


APP_NAME = 'PING-SPOT'
PAGES_DIR_NAME = 'pages'


MTR_ICON_SUCCESS = ':material/check_circle:'
MTR_ICON_INFO = ':material/info:'
MTR_ICON_WARNING = ':material/warning:'
MTR_ICON_ERROR = ':material/error:'


class MessageIconMapper(Enum):
    success = MTR_ICON_SUCCESS
    info = MTR_ICON_INFO
    warning = MTR_ICON_WARNING
    error = MTR_ICON_ERROR


ATHENS_COORDS = (37.0816818, 23.5035676)
HUA_COORDS = (37.9623023, 23.6983667)
DEFAULT_MAP_CENTER = HUA_COORDS
DEFAULT_MAP_ZOOM = 18
DEFAULT_OFFSET = .001
DEFAULT_PATH_NUM_POINTS = .001


OSRM_API = 'http://router.project-osrm.org/route/v1/foot'


MARKER_COLORS = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
                 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
                 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
                 'gray', 'black', 'lightgray']


TIMEZONE = 'Europe/Athens'


COMMON_MAP_OPTIOS = {'polyline': False, 'marker':False, 'circlemarker':False, 'circle':False}


USER_EMOJIES = dict[('Grapes', '🍇'), ('Melon', '🍈'), ('Watermelon', '🍉'), ('Tangerine', '🍊'),
                    ('Lemon', '🍋'), ('Lime', '🍋‍🟩'), ('Banana', '🍌'), ('Pineapple', '🍍'),
                    ('Mango', '🥭'), ('Red Apple', '🍎'), ('Green Apple', '🍏'), ('Pear', '🍐'),
                    ('Peach', '🍑'), ('Cherries', '🍒'), ('Strawberry', '🍓'), ('Blueberries', '🫐'),
                    ('Kiwi Fruit', '🥝'), ('Tomato', '🍅'), ('Olive', '🫒'), ('Coconut', '🥥'),
                    ('Avocado', '🥑'), ('Eggplant', '🍆'), ('Potato', '🥔'), ('Carrot', '🥕'),
                    ('Ear of Corn', '🌽'), ('Hot Pepper', '🌶️'), ('Bell Pepper', '🫑'), ('Cucumber', '🥒'),
                    ('Leafy Green', '🥬'), ('Broccoli', '🥦'), ('Garlic', '🧄'), ('Onion', '🧅'),
                    ('Peanuts', '🥜'), ('Beans', '🫘'), ('Chestnut', '🌰'), ('Ginger Root', '🫚'),
                    ('Pea Pod', '🫛'), ('Brown Mushroom', '🍄‍🟫')]


# Dummy sample data for zones (GeoJSON format)
ZONE_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-0.1278, 51.5074],
                        [-0.1280, 51.5074],
                        [-0.1280, 51.5076],
                        [-0.1278, 51.5076],
                        [-0.1278, 51.5074]
                    ]
                ]
            },
            "properties": {"zone_name": "Polygon Zone", "color": "red"}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-0.1290, 51.5072],
                        [-0.1290, 51.5075],
                        [-0.1287, 51.5075],
                        [-0.1287, 51.5072],
                        [-0.1290, 51.5072]
                    ]
                ]
            },
            "properties": {"zone_name": "Rectangle Zone", "color": "blue"}
        }
    ]
}