from secrets import choice
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from .managers import CustomUserManager
# Create your models here.

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

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public Identifier')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email