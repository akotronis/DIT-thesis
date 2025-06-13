from django.contrib.auth import get_user_model
from rest_framework import serializers as drf_srl
from rest_framework_gis import serializers as gis_srl

from . import models as intr_mdl
from users import serializers as usr_mdl


class MessageModelSerializer(drf_srl.ModelSerializer):
    class Meta:
        model = intr_mdl.Message
        fields = '__all__'


class ZoneModelSerializer(gis_srl.GeoFeatureModelSerializer):
    class Meta:
        model = intr_mdl.Zone
        geo_field = 'polygon'
        fields = '__all__'


class LocationModelSerializer(gis_srl.GeoFeatureModelSerializer):
    email = drf_srl.EmailField(read_only=True, source='user.email')

    class Meta:
        model = intr_mdl.Location
        geo_field = 'point'
        fields = '__all__'


class LocationQueryParamSerializer(drf_srl.Serializer):
    start = drf_srl.DateTimeField(required=False)
    user_id = drf_srl.ListField(child=drf_srl.PrimaryKeyRelatedField(queryset=get_user_model().objects.all()), source='users', required=False)
    latest = drf_srl.IntegerField(required=False)
    mock = drf_srl.BooleanField(required=False)
    visible = drf_srl.BooleanField(required=False)

    def validate_mock(self, value):
        return value if 'mock' in self.context['request'].query_params else None

    def validate_visible(self, value):
        return value if 'visible' in self.context['request'].query_params else None


class NotificationModelSerializer(drf_srl.ModelSerializer):
    email = drf_srl.EmailField(read_only=True, source='user.email')
    zone_name = drf_srl.CharField(read_only=True, source='zone.name')
    group_name = drf_srl.CharField(read_only=True, source='zone.group.name')

    class Meta:
        model = intr_mdl.Notification
        fields = '__all__'


class NotificationQueryParamSerializer(drf_srl.Serializer):
    seen = drf_srl.BooleanField(required=False)

    def validate_seen(self, value):
        return value if 'seen' in self.context['request'].query_params else None