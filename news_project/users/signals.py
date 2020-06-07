from django.db.models.signals import post_save
from django.contrib.auth.models import User
from users.models import UserProfile


def create_admin_user_profile(created, instance, **kwargs):
    if created and instance.is_superuser:
        UserProfile.objects.create(user=instance, group='A')


post_save.connect(create_admin_user_profile, sender=User)