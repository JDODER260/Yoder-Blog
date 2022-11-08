from django import forms
from post.models import Post
from .models import Category
from chat.models import Chat
import django_filters

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Message Content', 'class': 'content-section'}),
            'person_to': forms.Select(attrs={'id': 'person_to', 'type': 'hidden', 'class': 'smallthings'}),
            'author': forms.Select(attrs={'id': 'author', 'type': 'hidden', 'class': 'smallthings'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'modwid', 'placeholder': 'Category Name'}),
        }



class HomeFilter(django_filters.FilterSet):
    class Meta:
        models = Post
        fields = ("Completed-requests", "Complaints", "Feature-Requests")