from django.db import models


class ContacUs(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "تماس با ما"
        verbose_name_plural = "تماس‌های با ما"
        ordering = ['-created_at']
    
    
    def __str__(self):
        return f"ContactUs from {self.name} <{self.email}>"
