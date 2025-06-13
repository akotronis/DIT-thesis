from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.gis.db import models as models


class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def truncated_text(self, to=30):
        return f'{(self.text or "")[:to]}...'

    def __str__(self):
        return f'({self.pk}) User: {self.user.email}, Group: ({self.group.pk} - {self.group.name}), {self.truncated_text()}'


class Zone(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=100)
    polygon = models.PolygonField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['group', 'name']

    def __str__(self):
        return f'({self.pk}) Name: {self.name}, Group: ({self.group.pk} - {self.group.name})'


class Location(models.Model):
    point = models.PointField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='locations')
    mock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.pk}) - {self.point.coords[::-1]}, {self.user.email}'


class Notification(models.Model):
    class Type(models.TextChoices):
        MESSAGE = 'MESSAGE'
        ENTRANCE = 'ENTRANCE'
        EXIT = 'EXIT'

    type = models.CharField(choices=Type.choices)
    message = models.OneToOneField(Message, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.pk}) {self.type}'