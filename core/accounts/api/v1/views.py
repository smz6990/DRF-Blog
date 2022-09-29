from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import SignUpModelSerializer, CustomAuthTokenSerializer
from .permissions import NotAuthenticated


class SignUpAPIView(generics.GenericAPIView):
    """
    Class for register a new User
    """

    serializer_class = SignUpModelSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "details": [
                "Your account created successfully.",
                "Your email is:",
                serializer.data.get("email", None),
            ]
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Class to customize the login token view (ObtainAuthToken)
    """

    serializer_class = CustomAuthTokenSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        data = {"token": token.key, "email": user.email, "id": user.pk}
        return Response(data)


class CustomLogOutDiscardToken(APIView):
    """
    Class that destroy the User token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
