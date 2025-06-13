from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    visible = models.BooleanField(default=True)
   
    # Field used as unique identifier
    USERNAME_FIELD = 'email'
    # Fields prompted for, when creating superuser
    # If username not included we get error since it is required
    REQUIRED_FIELDS = ['username']

    def field_iexact_exists(self, field_dict):
        field_dict = {f'{k}__iexact':v for k,v in field_dict.items()}
        # Make sure we are serching in users other than self: (update case)
        condition = models.Q(**field_dict) & ~models.Q(pk=self.pk)
        return self.__class__.objects.filter(condition).exists()

    def validate_unique(self, *args, **kwargs):
        errors = {}
        if self.field_iexact_exists({'email':self.email}):
            errors.update({'email': [ValidationError(['User with this Email address already exists.'])]})
        if self.field_iexact_exists({'username':self.username}):
            errors.update({'username': [ValidationError(['A user with that username already exists.'])]})
        if errors:
            raise ValidationError(errors)
        return super().validate_unique(*args, **kwargs)

    def __str__(self):
        return self.email
    

class Invitation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'

    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_invitations')
    guest = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_invitations')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.pk}) Host: {self.host.email}, Guest: {self.guest.email}, Group: ({self.group.pk} - {self.group.name}), {self.status}'
