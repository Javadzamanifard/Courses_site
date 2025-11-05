from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from .models import ContacUs

class ContactUs(TemplateView):
    template_name = 'pages/contact_us.html'


class AboutUs(TemplateView):
    template_name = 'pages/about.html'


class BecomeInstructor(TemplateView):
    template_name = 'pages/become_instructor.html'


class TermsAndConditions(TemplateView):
    template_name = 'pages/terms_conditions.html'


@login_required
def contact_us_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")
        if name and email and message_text:
            ContacUs.objects.create(name=name, email=email, message=message_text)
            messages.success(request, _("Your message was sent successfully."))
            return redirect("accounts:home")
        else:
            messages.error(request, _("All fields are required."))
    return render(request, "pages/contact_us.html")
