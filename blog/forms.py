from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title')

        return title