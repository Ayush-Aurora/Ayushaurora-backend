from django.shortcuts import render
from rest_framework import generics,status

from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class UserRegisterView(generics.GenericAPIView):

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self , request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data , status = status.HTTP_201_CREATED)