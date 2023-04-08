from rest_framework import serializers
from .models import User
from authentication import helper
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class GateSerializer(serializers.Serializer):
    cash = serializers.IntegerField()


class VerifySerializer(serializers.Serializer):
    verifyCode = serializers.IntegerField()
    phone = serializers.CharField(max_length=11)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20)


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=20)

    def create(self, validated_data):
        otp = helper.otp_generator()
        print(otp)
        phone_number = validated_data['phone']
        helper.send_otp(phone_number, otp)
        user = User.objects.create(phone=phone_number, password=validated_data['phone'], otp=otp, otp_create_time=timezone.now)
        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'id']

