from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/enrol', views.enrol_in_course, name='enroll'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
