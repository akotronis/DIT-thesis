import requests

from . import constants as intr_cnst
from . import models as intr_mdl


def check_for_zone_entrance(location, zone):
    previous_location = intr_mdl.Location.objects.filter(user=location.user, created_at__lt=location.created_at).order_by('-created_at').first()
    return all([
        zone.polygon.contains(location.point),
        not previous_location or not zone.polygon.contains(previous_location.point)
    ])


def check_for_zone_exit(location, zone):
    previous_location = intr_mdl.Location.objects.filter(user=location.user, created_at__lt=location.created_at).order_by('-created_at').first()
    return previous_location and all([
        not zone.polygon.contains(location.point),
        zone.polygon.contains(previous_location.point)
    ])


def zones_crossed(location, cross_function):
    groups = location.user.groups.all()
    group_zones = intr_mdl.Zone.objects.filter(group__in=groups)
    return [zone for zone in group_zones if cross_function(location, zone)]


def toggle_tapo_power_supply(*, on: bool=False):
    try:
        requests.post(intr_cnst.TAPO_WEBHOOK_ON_URL if on else intr_cnst.TAPO_WEBHOOK_OFF_URL)
        tapo_status ='ON' if on else 'OFF'
        print(f' Turning Home Assistant Tapo: {tapo_status} '.center(100, '='))
    except Exception as e:
        print(f' Error accessing Home Assistant '.center(100, '='))
        print(str(e))
