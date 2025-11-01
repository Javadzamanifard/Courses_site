from django.shortcuts import render,redirect
from django.views import generic

from .models import Profile

from .forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Profile.objects.select_related('user') 
    
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        profile_user = self.get_object().user
        context['profile_user'] = profile_user
        return context


@login_required
def profile_update_view(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been successfully updated.')
            return redirect(profile.get_absolute_url())
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profiles/profile_form.html', context)
