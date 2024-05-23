from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, UserCreationForm


class SigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }))

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password."
        ),
        "inactive": "This account is inactive."
    }


class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Old Password',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))

    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'style': 'width: 100%; height: 1.5rem; border-radius: 5px; padding: 10px;'
        }
    ))
