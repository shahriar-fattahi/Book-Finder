from typing import List

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import Book, Review


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
            if Review.objects.get(book_id=book_id, user_id=user_id):
                raise serializers.ValidationError({"error": ""})
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
