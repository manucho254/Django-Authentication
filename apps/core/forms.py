from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    Email = forms.EmailField(max_length=100, label="Email")
    password = forms.CharField(max_length=100, label="Password")
    confirm_password = forms.CharField(max_length=100, label="Confirm Password")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(max_length=100, label="Password")
