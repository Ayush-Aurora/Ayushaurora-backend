from django.shortcuts import render
from rest_framework import generics,status

from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt

from .models import User
from .utils import Utilities
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

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse("mail-verify")
        absolute_url = "http://"+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absolute_url
        data = {'email_body': email_body , 'email_subject': 'Email Verification for you' , 'to_email': user.email}
        Utilities.send_email(data)

        return Response(user_data , status = status.HTTP_201_CREATED)

class VerifyMailView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    def get(self , request):
        token = request.GET.get('token')
        try:
            jwt_payload = jwt.decode(token , settings.SECRET_KEY , algorithms='HS256')
            user = User.objects.get(id = jwt_payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'status': str(user.username) + ' verified successfully!'} , status=status.HTTP_200_OK)
            return Response({'status': str(user.username) + ' already verified!'} , status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'status': 'Verification Link Expired!'} , status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'status': 'Invalid Token'} , status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data , status = status.HTTP_200_OK)