from typing import List

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import Book


class ListBookApi(APIView):
    def get_queryset(self) -> List[Book]:
        genre = self.request.query_params.get("genre")
        if genre:
            return Book.objects.filter(genre=genre, user_id=self.request.user.id)
        return Book.objects.all()

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serialized_data = [book.model_dump() for book in queryset]
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK,
        )
