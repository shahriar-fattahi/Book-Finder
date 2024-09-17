from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SetCSRFCookieApi(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self, request: Request) -> Response:
        return Response("CSRF Cookie set.")


@method_decorator(csrf_protect, name="dispatch")
class LoginApi(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request: Request) -> Response:
        credentials_data = LoginSerializer(data=request.data)
        credentials_data.is_valid(raise_exception=True)
        user = authenticate(**credentials_data.data)
        if user is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request=request, user=user)
        return Response(
            data=UserSerializer(instance=user).data,
            status=status.HTTP_200_OK,
        )
