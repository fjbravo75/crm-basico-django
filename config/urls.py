"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from crm.management.commands.seed_demo_crm import DEMO_PASSWORD, DEMO_USER
from crm.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path("acceso/registro/", register, name="register"),
    path(
        "acceso/login/",
        LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
            extra_context={
                "demo_username": DEMO_USER["username"],
                "demo_password": DEMO_PASSWORD,
            },
        ),
        name="login",
    ),
    path("acceso/logout/", LogoutView.as_view(), name="logout"),
    path("", include("crm.urls")),
]
