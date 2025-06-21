BACKEND_PORT = 8000

BACKEND_HOSTS = [
    # Fixed container IP (Access through reverse proxies and wireguard tunnnel/traffic forwarding)
    '172.28.1.102',
    # Localhost (Mobile app runs locally)
    'localhost',
    '127.0.0.1',
    # Fixed container IP (Access through reverse proxies and wireguard tunnnel/traffic forwarding)
    '192.168.1.102',
]

LOCATION_TEMPLATE = """
    {{
        "type": "Feature",
        "geometry": {{
            "type": "Point",
            "coordinates": [
                {lon},
                {lat}
            ]
        }},
        "properties": {{
            "mock": {mock},
            "user": {user_id}
        }}
    }}
"""

SHARE_LOCATION_EVERY_SECS = 3

HUA_COORDS = (37.9623023, 23.6983667)
MOCK_START_POINT = HUA_COORDS
# Center of the square zone on the left of HUA_COORDS surrounded by Χανδρή/Κύπρου/Αρχιμήδου/Θεσσαλονίκης
MOCK_END_POINT = (37.96102287405596, 23.695562066717347)
MOCK_PATH_POINTS = [
    MOCK_START_POINT[::-1],
    [23.698255, 37.96227],
    [23.698072, 37.962665],
    [23.697322, 37.962462],
    [23.69629, 37.962105],
    [23.695757, 37.96194],
    [23.695178, 37.96175],
    MOCK_END_POINT[::-1]
]