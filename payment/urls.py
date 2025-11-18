# payment/urls.py
from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('request/', views.send_request, name='request'), 
    path('verify/', views.verify_payment, name='verify'),
]