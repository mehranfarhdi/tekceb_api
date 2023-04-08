from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
import os
import uuid
from django.db import models
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.myusermanager import MyUserManager



class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=11, unique=True)
    is_verified = models.BooleanField(default=False)
    verifyCode = models.PositiveIntegerField(blank=True, null=True)
    verifyCode_create_time = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
