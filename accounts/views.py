from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login

from .forms import CustomSignupForm

from allauth.account.views import PasswordResetView, PasswordResetFromKeyView

from django.contrib import messages

class CustomSignUpView(generic.CreateView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save(self.request)
        login(self.request, user)
        messages.success(self.request, 'You have successfully logged in.')
        return redirect(self.success_url)


def homeview(request):
    return render(request, 'accounts/home.html')


class CustomPasswordRest(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    success_url = reverse_lazy('password_reset_complete')