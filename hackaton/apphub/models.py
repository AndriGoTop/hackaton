from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    # telegram_id = models.CharField(max_length=64, blank=True, null=True)
    def __str__(self):
        return self.username