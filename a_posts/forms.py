from django import forms
from .models import Post, Response

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'category': forms.Select(choices=Post.TYPE),
        }


class ResponseCreateForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add response ...', 'rows': 3,'class': 'bg-slate-100 resize-none rounded-lg border-transparent active:ring-2 active:ring-slate-500 active:ring-offset-2 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2'}),
        }      

        label = {
            'content': '',
            }  
