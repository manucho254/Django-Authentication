from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import request, response
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm


class LoginView(View):
    def get(self, request: request.HttpRequest, *args, **kwargs):
        form = LoginForm()
        return render(request, "login.html", {form: form})

    def post(self, request: request.HttpRequest, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data.get("username")
            password: str = form.cleaned_data.get("password")

            auth_user = authenticate(username=username, password=password)

            if not auth_user:
                messages.error(request, "Invalid credentials, please try again.")
                return redirect("login")

            messages.success(request, "Logged in successfully.")
            login(request, auth_user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("login")


class LogoutView(View):
    def get(self, request: request.HttpRequest, *args, **kwargs):
        logout(request)
        redirect("login")


class RegisterView(View):
    def get(self, request: request.HttpRequest, *args, **kwargs):
        form = RegisterForm()
        return render(request, "register.html", {form: form})

    def post(self, request: request.HttpRequest, *args, **kwargs):

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

            user: User = User.objects.create_user(username, email, password)
            messages.success(request, "User registration successful.")
            return redirect("login")

        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("register")


class DashboardView(LoginRequiredMixin, View):
    redirect_field_name = None

    def get(self, request: request.HttpRequest, *args, **kwargs):
        context = {"user": request.user}
        return render(request, "dashboard.html", context)


def login_view(request: request.HttpRequest, *args, **kwargs) -> response.HttpResponse:

    if request.method != "POST":
        form = LoginForm()
        context = {"form": form}
        return render(request, "login.html", context)

    form = LoginForm(request.POST)

    if form.is_valid():
        username: str = form.cleaned_data.get("username")
        password: str = form.cleaned_data.get("password")

        auth_user = authenticate(username=username, password=password)

        if not auth_user:
            messages.error(request, "Invalid credentials, please try again.")
            return redirect("login")

        messages.success(request, "Logged in successfully.")
        login(request, auth_user)
        return redirect("dashboard")
    else:
        messages.error(request, "Invalid data provided, please try again.")
        return redirect("login")


def register_view(request: request.HttpRequest, *args, **kwargs):

    if request.method != "POST":
        form = RegisterForm()
        context = {"form": form}
        return render(request, "register.html", context)

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

        user: User = User.objects.create_user(username, email, password)
        messages.success(request, "User registration successful.")
        return redirect("login")
    
    else:
        messages.error(request, "Invalid data provided, please try again.")
        return redirect("register")


def logout_view(request: request.HttpRequest, *args, **kwargs):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required
def dashboard_view(request: request.HttpRequest, *args, **kwargs):
    user: User = request.user

    context = {"user": user}
    return render(request, "dashboard.html", context)
