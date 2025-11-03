from django.shortcuts import render
from django.views import generic

from .models import Course


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    
    def get_queryset(self):
        return Course.objects.all().filter(is_active=True).order_by('-created_at')
