from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from accounts.models import Profile
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
