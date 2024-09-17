from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SetCSRFCookie(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self, request: Request) -> Response:
        return Response("CSRF Cookie set.")
