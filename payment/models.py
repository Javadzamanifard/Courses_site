from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

from courses.models import Course


from django_jalali.db import models as jmodels

class PaymentTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('کاربر'))
    course_slugs_json = models.TextField(verbose_name=_("اسلاگ دوره‌های سبد خرید"))
    amount = models.PositiveIntegerField(verbose_name=_("مبلغ (تومان)"))
    authority = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("کد اعتبار سنجی زرین پال"))
    ref_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("کد پیگیری پرداخت"))
    is_paid = models.BooleanField(default=False, verbose_name=_("پرداخت شده"))
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    
    
    class Meta:
        verbose_name = _("تراکنش")
        verbose_name_plural = _("تراکنش‌ها")
    
    
    def __str__(self):  
        return f"Tnx {self.id} for {self.user.username}"
