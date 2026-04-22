# userprofile/forms.py
from django import forms

class AddFriendForm(forms.Form):
    # 只需要一個欄位：輸入對方的 ID
    target_id = forms.IntegerField(
        label='輸入特工編號 (ID)',
        widget=forms.NumberInput(attrs={
            'class': 'ID-input', 
        })
    )

