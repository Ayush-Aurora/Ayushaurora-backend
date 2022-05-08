from rest_framework import serializers
from .models import User

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
        role = attrs.get('role' , None)
        if role < 1 or role > 4:
            raise serializers.ValidationError(
                self.default_error_messages)
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

