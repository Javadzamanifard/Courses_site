from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'dicount_type', 'discount_value', 'valid_from', 'valid_to', 'uses_count', 'uses_limit', 'active')
    list_filter = ('active', 'valid_from', 'valid_to', 'dicount_type')
    search_fields = ('code',)
    ordering = ('-valid_from',)
