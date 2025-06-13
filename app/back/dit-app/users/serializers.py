from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.serializers import ModelSerializer

from . import models as usr_mdl
from interactions import serializers as intr_srl


class CustomAuthTokenSerializer(AuthTokenSerializer):
    email = serializers.EmailField(label='Email', write_only=True)
    username = serializers.CharField(required=False, read_only=True)

    def validate(self, attrs):
        # Obtain from email case insensitive
        attrs['username'] = attrs['email'].lower()
        return super().validate(attrs)


class UserModelSerializer(ModelSerializer):
    username = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'token', 'visible']

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if getattr(self.context.get('request'), 'method', None) != 'POST':
            ret.pop('token', None)
        return ret

    def validate_email(self, value):
        value = value.lower()
        if self.Meta.model.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value
        
    def validate(self, data):
        if 'email' in data:
            data['username'] = data['email'].lower()
        return super().validate(data)
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    

class GroupModelSerializer(ModelSerializer):
    users = serializers.SerializerMethodField()
    zones = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'users', 'zones']

    def get_users(self, obj):
        return UserModelSerializer(obj.user_set.all(), many=True).data
    
    def get_zones(self, obj):
        return intr_srl.ZoneModelSerializer(obj.zones.all(), many=True).data
    
    def create(self, validated_data):
        group = super().create(validated_data)
        group.user_set.add(self.context['request'].user)
        return group
    

class InvitationModelSerializer(ModelSerializer):
    guest = serializers.EmailField()
    host = serializers.EmailField(source='host.email', read_only=True)
    _group = serializers.SerializerMethodField()

    class Meta:
        model = usr_mdl.Invitation
        fields = '__all__'

    def get__group(self, obj):
        return GroupModelSerializer(obj.group).data

    def validate_guest(self, value):
        if not (user := get_user_model().objects.filter(email=value).first()):
            raise serializers.ValidationError('Unknown user. Check the email address.')
        return user
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['group'] = ret.pop('_group')
        return ret
    
    def validate(self, data):
        request = self.context.get('request')
        method = getattr(request, 'method', None)
        group, guest = map(data.get, ['group', 'guest'])
        if guest and guest in group.user_set.all():
            raise serializers.ValidationError(f'User {guest.email} is already in group "{group.name}"')
        host = getattr(self.context.get('request'), 'user', None)
        if method == 'POST':
            data['host'] = host
            if host not in group.user_set.all():
                raise serializers.ValidationError(f'Host is not a member of group "{group.name}"')
        return super().validate(data)
    
    def update(self, instance, validated_data):
        if validated_data.get('status') == self.Meta.model.Status.ACCEPTED.value:
            instance.group.user_set.add(self.context['request'].user)
        return super().update(instance, validated_data)
