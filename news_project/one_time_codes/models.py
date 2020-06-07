import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class OneTimeCode(models.Model):

    code = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='one_time_codes',
    )
    is_confirmed = models.BooleanField(default=False)

    @property
    def is_active(self):
        return timezone.localtime() - timezone.timedelta(hours=settings.ONE_TIME_CODE_LIFETIME_HOURS) < self.date

    def __str__(self):
        if self.is_confirmed:
            return f'Confirmed code {self.code} for {self.user.username}, {self.date}'
        return f'Not confirmed code {self.code} for {self.user.username}, {self.date}'
