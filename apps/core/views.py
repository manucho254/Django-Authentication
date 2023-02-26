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
            

            if not username or not password:
                messages.error(
                    request,
                    "Username, password needed, please try again.",
                )
                return redirect("login")

            auth_user = authenticate(username=username, password=password)

            if not auth_user:
                messages.error(request, "User not found, please try again.")
                return redirect("login")
            else:
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

            if not username or not password or not confirm_password:
                messages.error(
                    request,
                    "Username, password and confirm_password needed, please try again.",
                )
                return redirect("register")

            user: User = User.objects.filter(username=username).first()

            if user:
                messages.error(
                    request, "Account with details provided exists, please try again."
                )
                return redirect("register")
            else:
                user: User = User.objects.create_user(username, email, password)
                user.set_password(password)
                user.save()

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

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data.get("username")
            password: str = form.cleaned_data.get("password")

            if not username or not password:
                messages.error(
                    request,
                    "Username, password needed, please try again.",
                )
                return redirect("login")

            auth_user = authenticate(username=username, password=password)

            if not auth_user:
                messages.error(request, "User not found, please try again.")
                return redirect("login")
            else:
                messages.success(request, "Logged in successfully.")
                login(request, auth_user)
                return redirect("dashboard")
        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("login")

    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {form: form})


def register_view(request: request.HttpRequest, *args, **kwargs):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data.get("username")
            email: str = form.cleaned_data.get("email")
            password: str = form.cleaned_data.get("password")
            confirm_password: str = form.cleaned_data.get("confirm_password")

            if not username or not password or not confirm_password:
                messages.error(
                    request,
                    "Username, password and confirm_password needed, please try again.",
                )
                return redirect("register")

            user: User = User.objects.filter(username=username).first()

            if user:
                messages.error(
                    request, "Account with details provided exists, please try again."
                )
                return redirect("register")
            else:
                user: User = User.objects.create_user(username, email, password)
                user.set_password(password)
                user.save()

                messages.success(request, "User registration successful.")
                return redirect("login")
        else:
            messages.error(request, "Invalid data provided, please try again.")
            return redirect("register")

    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {form: form})


def logout_view(request: request.HttpRequest, *args, **kwargs):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required(redirect_field_name=None)
def dashboard_view(request: request.HttpRequest, *args, **kwargs):
    user: User = request.user

    context = {"user": user}
    return render(request, "dashboard.html", context)
