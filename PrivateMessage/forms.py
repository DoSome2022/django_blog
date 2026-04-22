from django import forms
from .models import PrivateMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class':'id-input',
                'rows':3,
                'placeholder':  '輸入密語內容 (Whisper)...'
            }),
        }