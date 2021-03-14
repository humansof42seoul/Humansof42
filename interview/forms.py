from django import forms
from .models import Interview, Comment
from django_summernote.widgets import SummernoteWidget


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['title', 'interviewee', 'content', ]
        widgets = {'content': SummernoteWidget(), }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets= {'content': forms.Textarea(attrs={'class':'form-control', 'rows': 1}), }
