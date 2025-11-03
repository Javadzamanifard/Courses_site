from django.contrib import admin

from .models import Course, Lesson, Enrollment


# Create an inline admin interface for Lesson
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


# Register the Course model with the admin site
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'is_free', 'price', 'number_of_students', 'created_at', 'is_active']
    search_fields = ['title', 'instructor__username', 'is_free']
    list_filter = ['is_free', 'is_active', 'created_at']
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]


# Register the Enrollment model with the admin site
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at',]
    search_fields = ['student__username', 'course__title']
    list_filter = ['enrolled_at']
    ordering = ['-enrolled_at']