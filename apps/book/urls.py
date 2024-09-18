from django.urls import path

from .apis import ListBookApi

app_name = "book"

urlpatterns = [
    path("list/", ListBookApi.as_view(), name="list-book"),
]
