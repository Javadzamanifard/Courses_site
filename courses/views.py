from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from .models import Course, Enrollment, Comment
from .forms import CommentForm


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
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent__isnull=True, is_active=True)
        context['comment_form'] = CommentForm()
        return context
    
    
    def post(self, request, *args, **kwargs):
        course = self.get_object()
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
                comment.course = course
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comments = Comment.objects.filter(id=parent_id, course=course).first()
                if parent_comments:
                    comment.parent = parent_comments
            comment.save()
            messages.success(request, _('Your comment has been posted successfully!'))
        else:
            messages.error(request, _('There was an error posting your comment. Please try again.'))
        
        return redirect('courses:course_detail', slug=course.slug)


@login_required
def enrol_in_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    already_exists = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    if already_exists:
        messages.warning(request, _('You are already enrolled in this course'))
    else:
        Enrollment.objects.create(student=request.user, course=course)
        course.number_of_students += 1
        course.save()
        messages.success(request, _('Your registration was successful ✅'))
    return redirect('courses:course_detail', slug=course.slug)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    courses = [enrollment.course for enrollment in enrollments]
    return render(request, 'courses/my_courses.html', {'courses': courses})