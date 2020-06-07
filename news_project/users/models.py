from django.db import models
from django.contrib.auth.models import User
from one_time_codes.models import OneTimeCode


class UserProfile(models.Model):
    GROUPS = (
        ('U', 'User'),
        ('A', 'Admin'),
        ('E', 'Editor'),
    )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    group = models.CharField(max_length=1, choices=GROUPS, default='U')

    @property
    def email_confirmed(self):
        return bool(OneTimeCode.objects.filter(user=self.user, is_confirmed=True))

    def __str__(self):
        return f'profile of user {self.user.username}'
