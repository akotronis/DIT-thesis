from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.contrib.gis.forms import widgets

from . import models as intr_mdl


class ZoneAdmin(admin.OSMGeoAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Fetch the object to get its polygon
        obj = self.get_object(request, object_id)
        if obj and obj.polygon:
            # Get the centroid of the polygon
            centroid = obj.polygon.centroid
            # Set map center dynamically
            self.default_lon = centroid.x
            self.default_lat = centroid.y
        return super().change_view(request, object_id, form_url, extra_context)


class CustomOSMWidget(widgets.OSMWidget):
    class Media:
        css = {'all': ('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css')}
        js = ['https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js']


class LocationAdmin(admin.OSMGeoAdmin):
    formfield_overrides = {models.PointField: {'widget': CustomOSMWidget}}


admin.site.register(intr_mdl.Message)
admin.site.register(intr_mdl.Zone, ZoneAdmin)
admin.site.register(intr_mdl.Location, LocationAdmin)
admin.site.register(intr_mdl.Notification)