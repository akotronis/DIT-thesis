from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models as intr_mdl
from . import services as intr_srv


@receiver(post_save, sender=intr_mdl.Location)
def create_notification(sender, instance, created, **kwargs):
    if not instance.user.visible:
        return
    if created:
        zones_entered = intr_srv.zones_crossed(instance, intr_srv.check_for_zone_entrance)
        turned_on = False
        for zone in zones_entered:
            intr_mdl.Notification.objects.create(type=intr_mdl.Notification.Type.ENTRANCE, user=instance.user, zone=zone)
            if not turned_on:
                intr_srv.toggle_tapo_power_supply(on=True)
                turned_on = True
        zones_exited = intr_srv.zones_crossed(instance, intr_srv.check_for_zone_exit)
        turned_off = False
        for zone in zones_exited:
            intr_mdl.Notification.objects.create(type=intr_mdl.Notification.Type.EXIT, user=instance.user, zone=zone)
            if not turned_off:
                intr_srv.toggle_tapo_power_supply(on=False)
                turned_off = True