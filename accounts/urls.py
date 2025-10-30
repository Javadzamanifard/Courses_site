from django.urls import path
from .views import CustomSignUpView, homeview

app_name='accounts'

urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name='custom_signup'),
    path('home/', homeview, name='home'),
]
