from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models as usr_mdl
from . import permissions as usr_prm
from . import serializers as usr_srl


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = usr_srl.CustomAuthTokenSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id':user.pk, 'token': token.key})


class UserModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = get_user_model().objects.all().order_by('id')
    serializer_class = usr_srl.UserModelSerializer
    permission_classes = [usr_prm.UserPermissions]


class GroupModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = Group.objects.all().order_by('id')
    serializer_class = usr_srl.GroupModelSerializer

    def get_queryset(self):
        return self.request.user.groups.all()

    def partial_update(self, request, *args, **kwargs):
        if bool(request.query_params.get('leave')):
            obj = self.get_object()
            obj.user_set.remove(request.user)
            return Response({f'Successfully left group {obj.name}'})
        return super().partial_update(request, *args, **kwargs)


class InvitationModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = usr_mdl.Invitation.objects.all().order_by('-updated_at')
    serializer_class = usr_srl.InvitationModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().all()
        type_ = self.request.query_params.get('type', '').lower()
        if type_ == 'host':
            return queryset.filter(host=self.request.user).all()
        if type_ == 'guest':
            return queryset.filter(guest=self.request.user).all()
        return queryset.filter(Q(host=self.request.user) | Q(guest=self.request.user)).all()