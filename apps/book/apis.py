from typing import List

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import Book


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
