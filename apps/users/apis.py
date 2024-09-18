from knox.views import LoginView
from rest_framework.authentication import BasicAuthentication


class LoginApi(LoginView):
    authentication_classes = [BasicAuthentication]
