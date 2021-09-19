from django import forms
from .models import Post, Category

from tinymce import TinyMCE

class PostForm(forms.ModelForm):

    content = forms.CharField(
        widget=TinyMCE(attrs={
            'required': True,
            'cols': 30,
            'rows':10
        }))
    
    class Meta:
        model =  Post
        fields = ['title', 'content', 'category', 'cover_pic'] 

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name']


