from django.urls import include, path

from .apis import CreateReviewApi, DeleteReviewApi, ListBookApi, UpdateReviewApi

app_name = "book"

review_urls = [
    path("create/", CreateReviewApi.as_view(), name="add-review"),
    path("<int:review_id>/update/", UpdateReviewApi.as_view(), name="update-review"),
    path("<int:review_id>/delete/", DeleteReviewApi.as_view(), name="delete-review"),
]

urlpatterns = [
    path("list/", ListBookApi.as_view(), name="list-book"),
    path("review/", include(review_urls)),
]
