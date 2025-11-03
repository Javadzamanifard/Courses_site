from django.contrib import admin
from .models import ContacUs

from jalali_date.admin import ModelAdminJalaliMixin

@admin.register(ContacUs)
class ContactMessageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'message', 'created_at']
    ordering = ['-created_at']
