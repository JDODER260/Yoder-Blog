from django import forms
from main.models import Category
from .models import Post, Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        choices = Category.objects.all().values_list('name', 'name')
        choice_list = []
        for item in choices:
            choice_list.append(item)
        model = Post
        fields = ('title', 'category', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'modwid', 'placeholder': 'Content'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'modwid'}),
        }
        
