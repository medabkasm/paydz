from django.db.models.signals import post_save ,post_delete
from django.dispatch import receiver
from offers.models import Offer
from .models import Notification , Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Offer)
def create_new_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(notif=instance)

@receiver(post_save, sender=Offer)
def save_new_message(sender, instance,**kwargs):
    instance.notification.type = "notification"
    instance.notification.save()

    '''channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "AdminGroup",
        {
            "type": "new.notification",
            "message": "new notification"
        }
    )'''

@receiver(post_delete, sender=Offer)
def delete_offer(sender,instance,**kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "AdminGroup",
        {
            "type": "new.notification",
            "message": "new notification"
        }
    )



@receiver(post_save, sender=Message)
def create_new_msgNotification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(msg=instance)

@receiver(post_save, sender=Message)
def save_new_msgNotification(sender, instance, **kwargs):
    instance.notification.type = "message"
    instance.notification.save()
    '''channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "AdminGroup",
        {
            "type": "new.message",
            "message": "new message"
        }
    )'''

@receiver(post_delete, sender=Message)
def delete_message(sender,instance,**kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "AdminGroup",
        {
        "type": "new.message",
        "message": "new message"
        }
    )
