from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _
#from allauth.account.forms import SignupForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField()

class ResetRequestForm(forms.Form):
    username = forms.EmailField()


class ResetPassowrdForm(forms.Form):
    
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)