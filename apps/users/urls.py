from django.urls import path

from .apis import SetCSRFCookie

app_name = "users"

urlpatterns = [
    # path('login/', login_view, name='login'),
    path("csrf-token/", SetCSRFCookie.as_view(), name="set-csrf-token"),
]
