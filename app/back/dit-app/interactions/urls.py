from django.urls import path, include
from rest_framework import routers

from . import views as intr_vw


app_name = 'interactions'

router = routers.DefaultRouter(trailing_slash=False)
router.register('messages', intr_vw.MessageModelViewSet, basename='messages')
router.register('zones', intr_vw.ZoneModelViewSet, basename='zones')
router.register('locations', intr_vw.LocationModelViewSet, basename='locations')
router.register('notifications', intr_vw.NotificationModelViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]