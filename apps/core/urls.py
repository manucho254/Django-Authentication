from django.urls import path

from . import views


urlpatterns = [
    # class based views
    # path("login/", views.LoginView.as_view(), name="login"),
    # path("register/", views.RegisterView.as_view(), name="register"),
    # path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # path("logout/", views.LogoutView.as_view(), name="logout"),
    # function based
    path("auth/register/", views.register_view, name="register"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("auth/confirm-email/<str:token>/", views.confirm_account_view, name="confirm-email"),
    path("auth/change-password/<str:token>/", views.change_password_view, name="change-password"),
    path("auth/reset-password/", views.reset_password_view, name="reset-password"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
