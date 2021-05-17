from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .models import UserAuth


class UserCreate(generics.CreateAPIView):
    """Create a new User."""
    description = 'This route is used to create a new User.'
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(generics.CreateAPIView):
    """Do login"""
    description = 'This route is used to login a User.'
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = UserAuth().do_login(request, request.data)
            data = UserLoginSerializer(user).data
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
