# forms.py
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class UserAuthenticationForm(forms.Form):
    username = forms.CharField(label='Email address or Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

    def get_user(self):
        return self.user
    

class UserSignupForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address'
    }))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.is_active = False
            user.save()
        return user
    

class UserPasswordResetForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'class': 'form-control py-3'
    }))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email does not exist!")
        return email


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'class': 'mt-3 p-2', 'placeholder': 'Create Password'
    }))
    new_password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput(attrs={
        'class': 'mt-3 p-2', 'placeholder': 'Password Confirmation'
    }))

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "The two password fields didn’t match.")
        return password2

    

