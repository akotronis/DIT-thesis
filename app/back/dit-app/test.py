def setup():
    try:
        import os
        import django
        settings_var_name = 'DJANGO_SETTINGS_MODULE'
        os.environ.setdefault(settings_var_name, 'project.settings')
        django.setup()
    except RuntimeError:
        pass
setup()

import random
import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.gis.geos import Point, Polygon

from interactions.models import Zone, Location


########################################################################################################
########################################################################################################
# HUA_COORDS = (37.9623023, 23.6983667)
# HUA_COORDS = HUA_COORDS[::-1]
# user = get_user_model().objects.filter(is_superuser=True).first()
# group = Group.objects.first()
# offset = 0.001
# for i in range(5):
#     a = (HUA_COORDS[0] + i * offset, HUA_COORDS[1] + i * offset)
#     x, y = a
#     b = (x, y + offset)
#     c = (x + offset, y + offset)
#     d = (x + offset, y)
#     e = a

#     polygon = Polygon((a, b, c, d, e))
#     zone = Zone.objects.create(group=group, name=f'Zone - gr{group.pk}-{int(time.time() * 1_000_000)}', polygon=polygon)
#     print(zone)

#     point = Point(x - i * offset, y - i * offset)
#     loc = Location.objects.create(point=point, user=user)
#     print(loc)
########################################################################################################
########################################################################################################
points = [(23.6983667, 37.9623023), [23.698255, 37.96227], [23.698072, 37.962665], [23.698624, 37.962847], (23.69876966666667, 37.96257233333334)]
users = ['ak@email.com', 'ak-01@email.com']
users = list(get_user_model().objects.filter(email__in=users).all())

for i, point in enumerate(points):
    user = users[i % 2]
    _point = Point(*point)
    Location.objects.create(point=_point, user=user)
    time.sleep(3)
