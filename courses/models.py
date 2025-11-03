from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from ckeditor.fields import RichTextField

from django_jalali.db import models as jmodels


# Create Course model
class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("عنوان دوره"))
    description = RichTextField(verbose_name=_("توضیحات دوره"))
    short_description = models.TextField(max_length=500, verbose_name=_("توضیحات کوتاه دوره"))
    instructor = models.ForeignKey(
                    settings.AUTH_USER_MODEL, 
                    on_delete=models.PROTECT, 
                    related_name = "courses", 
                    verbose_name=_("مدرس دوره")
                    )
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name=_("تاریخ بروزرسانی"))
    price = models.PositiveIntegerField(verbose_name=_("قیمت دوره (به تومان)"))
    is_free = models.BooleanField(default=False, verbose_name=_("رایگان بودن دوره"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال بودن دوره"))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_("اسلاگ دوره"))
    preview_video = models.FileField(
                upload_to='courses/previews/', 
                blank=True, 
                null=True, 
                verbose_name=_("ویدئو پیش نمایش دوره")
                )
    cover_image = models.ImageField(
                    upload_to='courses/covers/', 
                    blank=True, 
                    null=True, 
                    verbose_name=_("تصویر کاور دوره")
                    )
    number_of_students = models.PositiveIntegerField(default=0, verbose_name=_("تعداد دانشجویان"))
    
    
    class Meta:
        verbose_name = _("دوره")
        verbose_name_plural = _("دوره‌ها")
        ordering = ['-created_at']
    
    
    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_free:
            self.price = 0
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})


# Create Lesson model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name=_("دوره"))
    title = models.CharField(max_length=255, verbose_name=_("عنوان درس"))
    content = RichTextField(verbose_name=_("محتوای درس"))
    video = models.FileField(upload_to='courses/lessons/videos/', verbose_name=_("ویدئو درس"))
    duration = models.DurationField(verbose_name=_("مدت زمان درس"))
    order = models.PositiveIntegerField(verbose_name=_("ترتیب درس"))
    
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    
    class Meta:
        verbose_name = _("درس")
        verbose_name_plural = _("درس‌ها")
        ordering = ['order']


# Create Enrollment model
class Enrollment(models.Model):
    student = models.ForeignKey(
                settings.AUTH_USER_MODEL, 
                on_delete=models.CASCADE, 
                related_name='enrollments', 
                verbose_name=_("دانشجو")
                )
    course = models.ForeignKey(
                Course, 
                on_delete=models.CASCADE, 
                related_name='enrollments', 
                verbose_name=_("دوره")
                )
    enrolled_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت‌نام"))
    
    
    class Meta:
        verbose_name = _("ثبت‌نام")
        verbose_name_plural = _("ثبت‌نام‌ها")
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']
    
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"