from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    useable_password = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11,)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
