from django.shortcuts import render
from django.views import generic

from .models import Profile


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
