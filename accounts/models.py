from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext as _

class CustomUser(AbstractUser):
    useable_password = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name=_('phone_number'))
    is_instructor = models.BooleanField(default=False, verbose_name=_('Im instructor'))
    is_student = models.BooleanField(default=True, verbose_name=_('Im student'))
    
    def __str__(self):
        return self.username
