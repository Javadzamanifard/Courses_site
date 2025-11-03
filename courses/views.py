from django.shortcuts import render
from django.views import generic

from .models import Course


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        course_type = self.request.GET.get('type', None)
        if course_type == 'free':
            return Course.objects.filter(is_active=True, is_free=True).order_by('-created_at')
        elif course_type == 'paid':
            return Course.objects.filter(is_active=True, is_free=False).order_by('-created_at')
        return Course.objects.all().filter(is_active=True).order_by('-created_at')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_type'] = self.request.GET.get('type', None)
        return context