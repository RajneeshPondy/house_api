from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

from users.models import Profile

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile has been created for user : {instance.username}")


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    username = f"{instance.first_name}_{instance.last_name}".lower()

    counter = 1
    while User.objects.filter(username=username):
        username = f"{instance.first_name}_{instance.last_name}_{counter}".lower()
        counter += 1
    instance.username = username
