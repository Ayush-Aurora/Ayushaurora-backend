from django.utils import timezone
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 10 , min_length = 6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters',
        'role': 'Role not defined in the system'}

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password' , 'role']

    def validate(self , attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        role = attrs.get('role' , 3)
        if role < 1 or role > 4:
            raise serializers.ValidationError(
                self.default_error_messages)
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255 , min_length=3)
    password = serializers.CharField(max_length = 10 , min_length=6 , write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length = 68 , min_length = 6 , read_only=True)
    # role = serializers.PositiveSmallIntegerField(read_only=True)
    class Meta:
        model = User
        fields = ['username' , 'email' , 'password' , 'tokens' , 'role']

    def validate(self, attrs):
        email = attrs.get('email' , '')
        password = attrs.get('password' , '')

        user = authenticate(email=email , password = password)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials, try again!')

        if not user.is_active:
            raise AuthenticationFailed('Your account has been disabled! Contact System Admin!')

        if not user.is_verified:
            raise AuthenticationFailed('Your Email is not verified, contact System Admin!')

        user.last_login = timezone.now()
        user.save()

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
            'role': user.role
        }
        



