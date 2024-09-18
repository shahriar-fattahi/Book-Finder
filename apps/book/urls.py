from django.urls import include, path

from .apis import CreateReviewApi, ListBookApi

app_name = "book"

review_urls = [
    path("create/", CreateReviewApi.as_view(), name="add-review"),
]

urlpatterns = [
    path("list/", ListBookApi.as_view(), name="list-book"),
    path("review/", include(review_urls)),
]
