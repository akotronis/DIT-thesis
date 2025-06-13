from django.urls import path, include
from rest_framework import routers

from . import views as usr_vw


app_name = 'users'

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', usr_vw.UserModelViewSet, basename='users')
router.register('groups', usr_vw.GroupModelViewSet, basename='groups')
router.register('invitations', usr_vw.InvitationModelViewSet, basename='invitations')

urlpatterns = [
    path('authenticate', usr_vw.CustomObtainAuthToken.as_view(), name='authenticate'),
    path('', include(router.urls)),
]