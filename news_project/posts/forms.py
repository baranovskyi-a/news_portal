from django import forms
from .models import Post
# from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = ['title', 'body']
