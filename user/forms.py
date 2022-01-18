from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    email = forms.EmailField(label='email', max_length=32, widget=forms.Textarea)
    password = forms.CharField(labe='password', widget=forms.PasswordInput)

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        password = clean_data.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if not check_password(password, user.password):
                self.add_error('email', '')
                self.add_error('password', '유효하지 않은 이메일이거나 비밀번호가 틀렸습니다.')
            else:
                self.id = user.id

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

