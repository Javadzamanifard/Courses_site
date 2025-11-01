from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from .models import Profile

@receiver(post_save, sender=CustomUser)
def create_update_profile(sender, instance, created, **kwarg):
    if created:
        Profile.objects.create(user=instance)
    elif hasattr(instance, 'profile'):
        instance.objects.save()