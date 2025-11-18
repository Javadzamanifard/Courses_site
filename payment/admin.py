from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست تراکنش‌ها نمایش داده می‌شوند
    list_display = (
        'id', 
        'user',         
        'authority', 
        'is_paid', 
        'created_at',
        'course_slugs_json',
        'amount_toman',
    )
    
    # فیلدهای قابل جستجو
    search_fields = (
        'user__username',  # جستجو بر اساس نام کاربری
        'ref_id',          # جستجو بر اساس کد پیگیری
        'authority',       # جستجو بر اساس کد اعتبارسنجی
    )

    # فیلترهای کناری
    list_filter = (
        'is_paid', 
        'created_at',
    )
    
    readonly_fields = (
        'user', 
        'amount', 
        'authority', 
        'ref_id', 
        'created_at',
        'id',
        'course_slugs_json',
    )
    
    def amount_toman(self, obj):
        return f"{int(obj.amount / 10 ):,}"  # اضافه کردن کاما برای خوانایی
    amount_toman.short_description = _("مبلغ (تومان)")