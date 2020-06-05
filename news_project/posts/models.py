from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    STATUSES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('D', 'Declined'),
    )
    title = models.CharField(max_length=500)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    status = models.CharField(max_length=1, choices=STATUSES, default='P')
