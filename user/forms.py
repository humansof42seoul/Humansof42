from django import forms
from .models import User

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']