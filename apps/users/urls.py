from django.urls import path

from .apis import LoginApi, SetCSRFCookieApi

app_name = "users"

urlpatterns = [
    path("login/", LoginApi.as_view(), name="login"),
    path("csrf-token/", SetCSRFCookieApi.as_view(), name="set-csrf-token"),
]
