from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ValidationError
from .models import CustomUser
# from django.conf import settings

from allauth.account.forms import SignupForm

from .validations import validate_phone_number, normalize_phone_number

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


class CustomUserChangeForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


class CustomSignupForm(SignupForm):   
    phone_number = forms.CharField(
        max_length=15,
        label='Phone Number',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '09123456789',
            'class': 'form-control' 
        })
    )
    is_instructor = forms.BooleanField(
        required=False,
        label='Im instructor'
    )
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            normalize = normalize_phone_number(phone_number)
            #1
            try:
                validate_phone_number(normalize)
            except ValidationError as e:
                raise forms.ValidationError(e.message)
            #2
            if CustomUser.objects.filter(phone_number=normalize).exists():
                raise ValidationError('This number is already exists')
            
            return normalize
        else:
            raise forms.ValidationError('Phone number is required.')
    
    
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.is_instructor = self.cleaned_data.get('is_instructor')
        user.save()
        return user