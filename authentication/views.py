from sre_parse import State
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    VerifySerializer,
    PhoneSerializer,
    ResetPasswordSerializer, LogoutSerializer
)
from .models import User
from django.contrib.auth import login
from authentication import helper
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from rest_framework.views import APIView
from django.contrib import auth





class UserRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class VerifyApi(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        verifyCode = serializer.data['verifyCode']
        phone = serializer.data['phone']
        try:
            user = User.objects.get(phone=phone)
            if user.verifyCode == verifyCode:
                user.verifyCode = None
                user.last_login = timezone.now()
                user.is_verified = True
                user.save()
                refresh = RefreshToken.for_user(user)
                login(request, user)
                return Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid verifyCode OR No any active user found for given verifyCode"},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "No user with this phone!!"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(phone=phone)
            if user.is_verified:
                auth_user = auth.authenticate(phone=phone, password=password)
                if auth_user:
                    auth.login(request, auth_user)
                    refresh = RefreshToken.for_user(user)
                    return Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "error, Wrong password",
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                verifyCode = helper.verifyCode_generator()
                helper.send_verifyCode(phone, verifyCode)
                user.verifyCode = verifyCode
                user.verifyCode_create_time = timezone.now
                user.save()
                return Response({
                    "message": "Ok, verify it"
                }, status=201)
        except User.DoesNotExist:
            user = User.objects.create_user(phone=phone, password=password)
            verifyCode = helper.verifyCode_generator()
            helper.send_verifyCode(phone, verifyCode)
            user.verifyCode = verifyCode
            user.verifyCode_create_time = timezone.now
            user.save()
            return Response({
                "message": "Ok, verify it",
            }, status=status.HTTP_201_CREATED)


class VerifyPhoneApi(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        try:
            user = User.objects.get(phone=phone)
            verifyCode = helper.verifyCode_generator()
            helper.send_verifyCode(phone, verifyCode)
            user.verifyCode = verifyCode
            user.verifyCode_create_time = timezone.now
            user.save()
            return Response({
                "message": "Ok, verify it",
            }, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({
                "message": "error, user with this phone number does not exist.",
            }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApi(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        if request.user.is_authenticated:
            user = request.user
            user.set_password(password)
            user.save()
            return Response({
                "message": "Ok, your password changed.",
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "error, please login and try it again.",
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

