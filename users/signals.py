from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# when a user is saved, send a signal
# the signal is then received by the receiver (create_profile() function)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): # instance is the user
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()