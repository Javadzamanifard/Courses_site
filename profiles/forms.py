from django import forms

from accounts.models import CustomUser
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', ]
        help_texts = {
            'email': 'ایمیل باید منحصر به فرد باشد.',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'birth_date']
        widgets = {
                'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'درباره خودتان بنویسید...'}),
                'birth_date': forms.DateInput(attrs={'type': 'date'}),
                }
