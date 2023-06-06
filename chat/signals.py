from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, ChatNotification
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=ChatNotification)
def send_notification(sender, instance, created, **kwargs):
    print("in signal")
    if created:
        channel_layer = get_channel_layer()
        notification_obj = ChatNotification.objects.filter(is_seen=False, chat_sent_to=instance.chat_sent_to).count()

        user_id = str(instance.chat_sent_to.id)
        print("in signals")
        data = {
            'count':notification_obj
        }
        print(notification_obj)
        async_to_sync(channel_layer.group_send)(
            user_id, {
                'type':'send_notification',
                'value':json.dumps(data)
            }
        )
