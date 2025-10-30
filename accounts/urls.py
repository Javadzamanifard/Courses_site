from django.urls import path
from .views import CustomSignUpView

urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name='custom_signup'),
]
