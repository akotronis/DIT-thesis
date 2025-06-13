import functools
import operator

from django.db.models import Q
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework.viewsets import ModelViewSet

from . import models as intr_mdl
from . import serializers as intr_srl
from project import utils as prj_utl


class MessageModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = intr_mdl.Message.objects.all()
    serializer_class = intr_srl.MessageModelSerializer


class ZoneModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = intr_mdl.Zone.objects.all()
    serializer_class = intr_srl.ZoneModelSerializer
    pagination_class = GeoJsonPagination


class LocationModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = intr_mdl.Location.objects.select_related('user').all().order_by('-created_at')
    serializer_class = intr_srl.LocationModelSerializer
    pagination_class = GeoJsonPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = prj_utl.validate_from_request(intr_srl.LocationQueryParamSerializer, self.request, attr='query_params')
        users, start, latest, mock, visible = map(query_params.get, ['users', 'start', 'latest', 'mock', 'visible'])
        if mock is not None:
            queryset = queryset.filter(mock=mock)
        if visible is not None:
            queryset = queryset.filter(user__visible=visible)
        if start:
            queryset = queryset.filter(created_at__gte=start)
        if users and not latest:
            queryset = queryset.filter(user__in=users)
        elif not users and latest:
            queryset = queryset[:latest]
        elif users and latest:
            queryset = functools.reduce(operator.or_, [queryset.filter(user=user)[:latest] for user in users])
        return queryset


class NotificationModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = intr_mdl.Notification.objects.select_related('zone', 'zone__group').prefetch_related('user__groups').order_by('-created_at')
    serializer_class = intr_srl.NotificationModelSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = prj_utl.validate_from_request(intr_srl.NotificationQueryParamSerializer, self.request, attr='query_params')
        user = self.request.user
        user_groups = user.groups.all()
        zone_condition = Q(zone__isnull=False) & Q(zone__group__in=user_groups) & Q(user__visible=True)
        message_condition = Q(message__isnull=False) & Q(message__group__in=user_groups)
        queryset = queryset.filter(zone_condition | message_condition)
        seen = query_params.get('seen')
        if seen is not None:
            queryset = queryset.filter(seen=seen)
        return queryset