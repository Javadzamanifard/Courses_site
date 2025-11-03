from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify

import os
from PIL import Image

from ckeditor.fields import RichTextField
from django_jalali.db import models as jmodels

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # bio = models.CharField(max_length=255, blank=True)
    bio = RichTextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/user_profiles', blank=True, default='avatars/defaul.jpg')
    # birth_date = models.DateField(blank=True, null=True)
    birth_date = jmodels.jDateField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    
    
    def __str__(self):
        return self.user.username
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        try:
            if self.avatar and os.path.isfile(self.avatar.path):
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
        except Exception as e:
            print(f"خطا در پردازش تصویر پروفایل: {e}")
    
    
    @property
    def get_fullname(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return self.user.username
    
    
    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={'slug': self.slug})