from django.db import models
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None , role=3):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.role = role
        user.save()
        return user

    def create_superuser(self, username, email, password=None , role=1):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password , role)
        user.is_superuser = True
        user.is_staff = True
        user.role = 1
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    DOCTOR = 2
    PATIENT = 3
    PHARMACIST = 4

    ROLE_CHOICES = (
        (ADMIN, 'SysAdmin'),
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
        (PHARMACIST, 'Pharmacist')
    )

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        user_tokens = RefreshToken.for_user(self)
        return {
            'refresh_token': str(user_tokens),
            'access_token': str(user_tokens.access_token)
        }