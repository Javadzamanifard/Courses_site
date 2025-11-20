from django.db import models

from django_jalali.db import models as jmodels


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percent', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
    )
    
    code = models.CharField(max_length=20, unique=True)
    
    dicount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    valid_from = jmodels.jDateTimeField()
    valid_to = jmodels.jDateTimeField()
    uses_count = models.PositiveIntegerField(default=0)
    uses_limit = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = 'کوپن‌های تخفیف'
    
    
    def __str__(self):
        return self.code
    
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if self.active and self.valid_from <= now <= self.valid_to:
            if self.uses_limit is None or self.uses_count < self.uses_limit:
                return True
        return False
    
    
    def get_total_discount(self, price):
        if self.dicount_type == 'percent':
            return (self.discount_value / 100) * price
        elif self.dicount_type == 'fixed':
            return self.discount_value
        return 0
    
    
    def apply_coupon(self, price):
        if self.is_valid():
            discount = self.get_total_discount(price)
            self.uses_count += 1
            self.save()
            return max(int(price - discount), 0)
        return price