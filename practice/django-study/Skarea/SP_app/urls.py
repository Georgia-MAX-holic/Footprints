"""Skarea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path

from SP_app.views import AccountDeleteView, AccountDetailView, AccountUpdateView, hello_world, AccountCreateView
from django.contrib.auth.views import LoginView, LogoutView

app_name ="SP_app"

urlpatterns = [
    path('hello_world/', hello_world, name="hello_world"),
    
    path('login/', LoginView.as_view(template_name="SP_app/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    
    path("create/", AccountCreateView.as_view(), name="create"),
    path("detail/<int:pk>", AccountDetailView.as_view(), name="detail"),
    path("update/<int:pk>", AccountUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", AccountDeleteView.as_view(), name="delete"),
]
