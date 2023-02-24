from django.urls import path

from . import views


urlpatterns = [
    # class based views
    
    # path("login/", views.LoginView.as_view(), name="login"),
    # path("register/", views.RegisterView.as_view(), name="register"),
    # path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # path("logout/", views.LogoutView.as_view(), name="logout"),
    
    # function based
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("dashboard", views.dashboard_view, name="dashboard")
]
