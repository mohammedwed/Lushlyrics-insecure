from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Save full name as first_name and last_name if possible
        full_name = self.cleaned_data.get("full_name", "")
        names = full_name.split(" ", 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")