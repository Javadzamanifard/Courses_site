from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('wishlist/', views.WishlistListView.as_view(), name='wishlist_list'),
    path('wishlist/add/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<slug:slug>/enrol', views.enrol_in_course, name='enroll'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
