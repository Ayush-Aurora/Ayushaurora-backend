from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User,Prescriptions


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def create_user(self , validated_data):
        auth_user = User(validated_data['email'])
        auth_user.set_password(validated_data['password'])
        auth_user.save()
        return auth_user




class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'access',
            'refresh',
            'role'
        )
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self , validated_data):
        pass

    def update(self , instance , validated_data):
        pass

    def validate(self , data):
        email = data['email']
        password = data['password']
        print(password)
        user = authenticate(email=email , password=password)
        print(user)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'password': user.password,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriptions
        fields = (
            'patientid',
            'doctorid',
            'medid',
            'created'
        )
    
    def validate(self, data):
        patientdata = User.objects.filter(uid=data['patientid'])
        doctordata = User.objects.filter(uid=data['doctorid'])

        if(patientdata.role != 2 and doctordata.role != 3):
            raise serializers.ValidationError("Invalid request")
        
        
        

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(validated_data['username'], validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
'''