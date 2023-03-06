from django.urls import path

from . import views


urlpatterns = [
    # function based
    path("auth/register/", views.register_view, name="register"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/logout/", views.logout_view, name="logout"),
    path(
        "auth/confirm-email/<str:token>/",
        views.confirm_account_view,
        name="confirm-email",
    ),
    path(
        "auth/change-password/<str:token>/",
        views.change_password_view,
        name="change-password",
    ),
    path("auth/reset-password/", views.reset_password_view, name="reset-password"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
