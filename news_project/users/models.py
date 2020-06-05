from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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
