from django import forms


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'کد تخفیف را وارد کنید',
        'aria-label': 'Recipient\'s username', 
        'aria-describedby': 'button-addon2'
    }))