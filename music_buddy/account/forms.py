from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from validate_email import validate_email
from .models import *

class UserRegisterForm(UserCreationForm):
    

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            

            if commit:
                user.save()

            return user

class CreateBlogPostForm(forms.ModelForm):
    title = forms.CharField(max_length=64)
    body = forms.Textarea(attrs={'cols': 30, 'rows': 3})
    class Meta:
        model = Post
        fields = ['title', 'body']

class CreateCommentForm(forms.ModelForm):
    
    class Meta:
        model = ProfileComment
        fields = ['body']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['image']

class CreateSongCommentForm(forms.ModelForm):
    
    class Meta:
        model = SongComment
        fields = ['body']

class EditCommentForm(forms.ModelForm):

    class Meta:
        model = ProfileComment
        fields = ['body']

    
