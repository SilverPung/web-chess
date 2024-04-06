from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


login_atributes = 'form-control rounded-xl py-3 w-full bg-gray-300'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Nazwa Użytkownika'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': login_atributes, 'placeholder': 'Hasło'}))


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': login_atributes, 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': login_atributes, 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': login_atributes, 'placeholder': 'Confirm Password'}))