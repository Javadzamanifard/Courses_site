from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login

from .forms import CustomSignupForm


class CustomSignUpView(generic.CreateView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save(self.request)
        login(self.request, user)
        return redirect(self.success_url)