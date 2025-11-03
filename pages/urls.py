from django.urls import path

from .views import ContactUs, TermsAndConditions, AboutUs, contact_us_view

app_name = 'pages'
urlpatterns = [
    path('contact/', ContactUs.as_view(), name='contact_us'),
    path('terms/', TermsAndConditions.as_view(), name='terms_conditions'),
    path('about/', AboutUs.as_view(), name='about_us'),
    path('contact/submit/', contact_us_view, name='contact_us_submit'),
]
