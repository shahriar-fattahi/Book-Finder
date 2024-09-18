from django.urls import path
from knox import views

from .apis import LoginApi

app_name = "users"

urlpatterns = [
    path(r"login/", LoginApi.as_view(), name="login"),
    path(r"logout/", views.LogoutView.as_view(), name="logout"),
    path(r"logoutall/", views.LogoutAllView.as_view(), name="logoutall"),
]
