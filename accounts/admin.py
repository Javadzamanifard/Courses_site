from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'phone_number', 'is_instructor', 'is_student', 'is_staff']
    search_fields = ['username', 'email', 'phone_number', ]
    
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                'fields': ('phone_number', 'is_instructor', 'is_student', )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                'fields': ('phone_number', 'is_instructor', 'is_student', )
            },
        ),
    )