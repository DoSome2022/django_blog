from django import forms
from .models import PublicMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = PublicMessage
        fields = ['content' , 'image' , 'nickname']