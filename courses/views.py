from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from .models import Course


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        course_type = self.request.GET.get('type', None)
        q = self.request.GET.get('q', None)
        
        if q:
            keywords = q.split()
            combined_q = Q()
            for kw in keywords:
                combined_q &= (
                    Q(title__icontains=kw) | Q(description__icontains=kw)
                )
            return Course.objects.filter(combined_q)
        
        if course_type == 'free':
            return Course.objects.filter(is_active=True, is_free=True).order_by('-created_at')
        elif course_type == 'paid':
            return Course.objects.filter(is_active=True, is_free=False).order_by('-created_at')
        return Course.objects.all().filter(is_active=True).order_by('-created_at')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_type'] = self.request.GET.get('type', None)
        return context


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Course.objects.filter(is_active=True)