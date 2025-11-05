from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment-textarea form-control shadow-sm rounded-3 p-3',
                'rows': 4,
                'placeholder': _('Make your comment here '),
                'style': 'resize: none; transition: all 0.3s ease; border: 1px solid #d1d5db; font-family: Vazirmatn, sans-serif;',
            }),
            'parent': forms.HiddenInput(attrs={'id': 'parent_id'}),
        }
        labels = {
            'content': '',
        }
