from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    SignUpModelSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from .permissions import NotAuthenticated, IsOwner
from ...models import Profile


User = get_user_model()


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
        data = {
            "token": token.key,
            "email": user.email,
            "user_id": user.pk,
        }
        return Response(data)


class CustomLogOutDiscardToken(APIView):
    """
    Class that destroy the User token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Class to customize the TokenObtainPairView to return user email
    and id to tokens.
    """

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordUpdateAPIView(generics.UpdateAPIView):
    """
    View to change authenticated user's old_password with
    the given new_password
    """

    serializer_class = ChangePasswordSerializer
    http_method_names = ["put"]
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.data.get("old_password")
        if not self.object.check_password(old_password):
            return Response(
                {
                    "old_password": [
                        "Old password is wrong!",
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        data = {"detail": "Password successfully changed."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Class to retrieve and update user Profile
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
