from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    email = forms.EmailField(max_length=100, label="Email")
    password = forms.CharField(
        max_length=30, label="Password", widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        max_length=30, label="Confirm Password", widget=forms.PasswordInput
    )

    username.widget.attrs.update({"class": "auth-input"})
    email.widget.attrs.update({"class": "auth-input"})
    password.widget.attrs.update({"class": "auth-input"})
    confirm_password.widget.attrs.update({"class": "auth-input"})


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(
        max_length=30, label="Password", widget=forms.PasswordInput
    )

    username.widget.attrs.update({"class": "auth-input"})
    password.widget.attrs.update({"class": "auth-input"})


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        max_length=30, label="Password", widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        max_length=30, label="Confirm Password", widget=forms.PasswordInput
    )

    password.widget.attrs.update({"class": "auth-input"})
    confirm_password.widget.attrs.update({"class": "auth-input"})


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email")

    email.widget.attrs.update({"class": "auth-input"})
