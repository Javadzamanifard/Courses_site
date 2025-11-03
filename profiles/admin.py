from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import  Profile

from accounts.models import CustomUser

from jalali_date.admin import ModelAdminJalaliMixin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'

class CustomUserAdmin(ModelAdminJalaliMixin, BaseUserAdmin):
    # پروفایل اینلاین را مانند قبل اضافه می‌کنیم
    inlines = (ProfileInline,)
    fieldsets = (
        # بخش اول: اطلاعات ورود (بدون عنوان)
        (None, {'fields': ('username', 'password')}),
        
        # بخش دوم: اطلاعات شخصی با فیلدهای سفارشی شما
        ('اطلاعات شخصی', {'fields': (
            'first_name', 
            'last_name', 
            'email', 
            'phone_number',  # فیلد سفارشی شما
            'is_instructor',
            'is_student',
        )}),
        
        # بخش سوم: دسترسی‌ها (این بخش از کلاس پایه می‌آید و بهتر است باشد)
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        
        # بخش چهارم: تاریخ‌های مهم
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )

    # نکته تکمیلی: برای نمایش فیلدها در لیست کاربران
    list_display = ('username', 'email', 'phone_number', 'is_instructor', 'is_student', )
# ثبت نهایی مدل با کلاس ادمین سفارشی
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)


# admin.site.register(Profile)