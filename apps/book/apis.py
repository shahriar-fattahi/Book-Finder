from typing import List

from django.http import Http404
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import Book, Review
from .utils import recommend_based_on_genre


class ListBookApi(APIView):
    def get_queryset(self) -> List[Book]:
        limit = self.request.query_params.get("limit", 21)
        offset = self.request.query_params.get("offset", 0)
        genre = self.request.query_params.get("genre")
        if genre:
            return Book.objects.filter(
                genre=genre,
                user_id=self.request.user.id,
                limit=limit,
                offset=offset,
            )
        return Book.objects.all(
            user_id=self.request.user.id,
            limit=limit,
            offset=offset,
        )

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serialized_data = [book.model_dump() for book in queryset]
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK,
        )


class CreateReviewApi(APIView):
    class InputSerializer(serializers.Serializer):
        book_id = serializers.IntegerField(min_value=1, required=True)
        rating = serializers.IntegerField(max_value=5, min_value=1)

        def validate_book_id(self, book_id):
            if Book.objects.get(book_id=book_id) is None:
                raise serializers.ValidationError(
                    f"No book exists with the specified ID: {book_id}"
                )
            return book_id

        def validate(self, attrs):
            book_id = attrs["book_id"]
            user_id = self.context["request"].user.id
            review = Review.objects.get(book_id=book_id, user_id=user_id)
            if review:
                update_url = reverse(
                    "api:book:update-review", kwargs={"review_id": review.id}
                )
                raise serializers.ValidationError(
                    {
                        "error": f"You’ve already submitted a review for this book. Use this link to update it: {update_url}",
                    }
                )
            return super().validate(attrs)

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        response_data = Review.objects.create(
            user_id=request.user.id,
            book_id=serializer.validated_data["book_id"],
            rating=serializer.validated_data["rating"],
        )
        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED,
        )


class UpdateReviewApi(APIView):
    class InputSerializer(serializers.Serializer):
        rating = serializers.IntegerField(max_value=5, min_value=1)

    def get_object(self):
        review_id = self.kwargs["review_id"]
        review = Review.objects.get(review_id=review_id)

        if review is None or review.user.id != self.request.user.id:
            raise Http404

        return review

    def put(self, request: Request, review_id: int) -> Response:
        review = self.get_object()
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Review.objects.update(
            review_id=review.id, rating=serializer.validated_data["rating"]
        )
        return Response(status=status.HTTP_200_OK)


class DeleteReviewApi(APIView):
    def get_object(self):
        review_id = self.kwargs["review_id"]
        review = Review.objects.get(review_id=review_id)

        if review is None or review.user.id != self.request.user.id:
            raise Http404

        return review

    def delete(self, request: Request, review_id: int) -> Response:
        review = self.get_object()
        Review.objects.delete(review_id=review.id)
        return Response(status=status.HTTP_200_OK)


class SuggestBookApi(APIView):
    def get_queryset(self) -> List[Book]:
        limit = self.request.query_params.get("limit", 21)
        offset = self.request.query_params.get("offset", 0)
        books = recommend_based_on_genre(
            user_id=self.request.user.id,
            limit=limit,
            offset=offset,
        )

        return books

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset()
        if isinstance(queryset, str):
            serialized_data = {"detail": queryset}
        else:
            serialized_data = [book.model_dump() for book in queryset]
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK,
        )
