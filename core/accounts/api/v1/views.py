from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .serializers import SignUpModelSerializer


class SignUpAPIView(generics.GenericAPIView):
    """
    Class for register a new User
    """

    serializer_class = SignUpModelSerializer

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
