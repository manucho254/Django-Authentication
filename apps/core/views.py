from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from apps.core.models import User
from apps.core.forms import (
    RegisterForm,
    LoginForm,
    ChangePasswordForm,
    ResetPasswordForm,
)
from apps.utils.email_operations import confirm_account, reset_password
from apps.utils.tokens import generate_token, validate_token
from apps.utils.custom_exceptions import RequestError

from datetime import timedelta


def login_view(request: HttpRequest, *args, **kwargs):

    try:
        form = LoginForm()

        if request.method != "POST":
            return render(request, "login.html", {"form": form})

        form = LoginForm(request.POST)

        if form.is_valid():
            email: str = form.cleaned_data.get("email")
            password: str = form.cleaned_data.get("password")

            auth_user: User = authenticate(email=email, password=password)

            if not auth_user:
                messages.error(request, "Invalid credentials, please try again.")
                return redirect("login")
            if not auth_user.is_confirmed:
                messages.error(
                    request,
                    "Account not confirmed, please confirm your account to login.",
                )
                return redirect("login")

            messages.success(request, "Logged in successfully.")
            login(request, auth_user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("login")
    except RequestError as e:
        messages.error(request, "An error occurred, please try again.")
        return redirect("login")


def register_view(request: HttpRequest, *args, **kwargs):

    try:
        form = RegisterForm()

        if request.method != "POST":
            return render(request, "register.html", {"form": form})

        form = RegisterForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data.get("username")
            email: str = form.cleaned_data.get("email")
            password: str = form.cleaned_data.get("password")
            confirm_password: str = form.cleaned_data.get("confirm_password")

            if len(password) < 8 or len(confirm_password) < 8:
                messages.error(
                    request,
                    "Password should contain 8 or more characters.",
                )
                return redirect("register")

            if password != confirm_password:
                messages.error(
                    request,
                    "Password and confirm_password don't match.",
                )
                return redirect("register")

            user: User = User.objects.filter(username=username).first()

            if user:
                messages.error(
                    request, "Account with details provided exists, please try again."
                )
                return redirect("register")

            user: User = User.objects.create_user(email, password=password)
            user.username = username
            user.save()
            token = generate_token({"user_id": str(user.user_id)}, timedelta(days=3))
            data = {"username": username, "email": email, "token": token}
            confirm_account(data)
            messages.success(request, "User registration successful.")
            return redirect("login")

        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("register")
    except RequestError as e:
        messages.error(request, "An error occurred, please try again.")
        return redirect("register")


def logout_view(request: HttpRequest, *args, **kwargs):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


def confirm_account_view(request: HttpRequest, token: str, *args, **kwargs):

    try:
        decoded_token = validate_token(token)

        user: User = User.objects.filter(user_id=decoded_token["user_id"]).first()
        user.is_confirmed = True
        user.save()

        messages.success(
            request,
            "Account confirmed successfully.",
        )
        return redirect("login")
    except RequestError as e:
        # we can log this exceptions to the logger
        messages.success(request, "Token invalid or expired.")
        return redirect("login")


def reset_password_view(request: HttpRequest, *args, **kwargs):

    try:
        form = ResetPasswordForm()
        if request.method != "POST":
            return render(request, "reset_password.html", {"form": form})

        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")

            user: User = User.objects.filter(email=email).first()

            messages.success(
                request,
                "An email has will be sent is an account with associated email is found.",
            )
            if not user:
                return redirect("reset-password")

            token = generate_token({"user_id": str(user.user_id)}, timedelta(hours=3))
            data = {"username": user.username, "email": email, "token": token}
            reset_password(data)
            return redirect("reset-password")
        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("reset-password")
    except RequestError as e:
        messages.error(request, "An error occurred, please try again.")
        return redirect("reset-password")


def change_password_view(request: HttpRequest, token: str, *args, **kwargs):

    try:
        form = ChangePasswordForm()
        if request.method != "POST":
            return render(request, "change_password.html", {"form": form})

        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("password")

            if password != confirm_password:
                messages.success(request, "Passwords don't match.")
                return redirect("change-password")

            decoded_token = validate_token(token)

            if "user_id" not in decoded_token:
                messages.success(request, "Token invalid or expired.")
                return redirect("change-password")

            user: User = User.objects.filter(user_id=decoded_token["user_id"]).first()
            user.set_password(password)
            user.save()

            messages.success(
                request,
                "Password changed successfully.",
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid data provided , please try again.")
            return redirect("change-password", token)
    except RequestError as e:
        messages.error(request, "An error occurred, please try again.")
        return redirect("change-password", token)


@login_required
def dashboard_view(request: HttpRequest, *args, **kwargs):
    user: User = request.user

    context = {"user": user}
    return render(request, "dashboard.html", context)
