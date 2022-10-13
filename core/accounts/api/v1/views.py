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
from django.contrib.auth import update_session_auth_hash
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from .serializers import (
    SignUpModelSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ResendVerifyEmailSerializer,
    ResetPasswordSerializer,
    PasswordResetDoneSerializer,
)
from .permissions import (
    NotAuthenticated,
    IsOwner,
    IsVerify,
)
from ...models import Profile
from ...utils import EmailThreadSend


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
        email = serializer.data.get("email")
        data = {
            "details": [
                "Your account created successfully.",
                "Verification email send to your email",
                "Your email is:",
                email,
            ]
        }
        user = User.objects.get(email=email)
        token = str(AccessToken.for_user(user))
        message_obj = EmailMessage(
            "email/email-verification-api.tpl",
            {"token": token, "user": user},
            'noreply@salehmzh.ir',
            to=[email],
        )
        EmailThreadSend(message_obj).start()
        return Response(data, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Class to customize the login token view (ObtainAuthToken)
    """

    serializer_class = CustomAuthTokenSerializer
    permission_classes = [NotAuthenticated]

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
    permission_classes = [IsVerify]
    model = User

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
        update_session_auth_hash(request, self.object)
        data = {"detail": "Password successfully changed."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Class to retrieve and update user Profile
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsVerify, IsOwner]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class VerifyEmailTokenAPIView(APIView):
    """
    Class to verify a user by sent email
    """

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verify:
                user.is_verify = True
                user.save()
                return Response(
                    {"email": f"{user.email} Successfully activated"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"email": f"{user.email} has already activated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except jwt.ExpiredSignatureError:
            return Response(
                {"errors": "Activations link expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"errors": "Invalid Token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendVerifyEmailGenericAPIView(generics.GenericAPIView):
    """
    Class to resend the verification email.
    """

    serializer_class = ResendVerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        if user.is_verify:
            return Response(
                {"email": f"{user.email} has already activated"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = str(AccessToken.for_user(user))
        message_obj = EmailMessage(
            "email/email-verification-api.tpl",
            {"token": token, "user": user},
            "noreply@salehmzh.ir",
            to=[user.email],
        )
        EmailThreadSend(message_obj).start()
        data = {"detail": "verification email successfully sent"}
        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordGenericAPIView(generics.GenericAPIView):
    """
    View to send reset password email.
    """

    serializer_class = ResetPasswordSerializer

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token = str(AccessToken.for_user(user))
        email_object = EmailMessage(
            "email/reset-password-api.tpl",
            {"token": token, "user": user},
            "noreply@salehmzh.ir",
            to=[user.email],
        )
        EmailThreadSend(email_object).start()
        data = {"detail": "reset password email successfully sent"}
        return Response(data, status=status.HTTP_200_OK)


class PasswordResetDoneGenericAPIView(generics.GenericAPIView):
    """
    View to reset user password.
    """

    serializer_class = PasswordResetDoneSerializer

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def put(self, request, *args, **kwargs):
        token = kwargs.get("token")
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = User.objects.get(id=payload["user_id"])

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Reset password link expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid Token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        update_session_auth_hash(request, user)
        data = {"detail": "Password successfully changed."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
