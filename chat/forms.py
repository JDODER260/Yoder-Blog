from django import forms
from .models import Chat


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Message Content', 'class': 'content-section'}),
            'person_to': forms.Select(attrs={'id': 'person_to', 'type': 'hidden', 'class': 'smallthings'}),
            'author': forms.Select(attrs={'id': 'author', 'type': 'hidden', 'class': 'smallthings'}),
        }