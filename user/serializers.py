from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import UserAuth


class UserRegisterSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'token',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_token(self, obj):
        return Token.objects.get(user=obj).key

    def create(self, validated_data):
        return UserAuth().prepare_new_user(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'token',)
        extra_kwargs = {
            'email': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'password': {'write_only': True},
        }

    def get_token(self, obj):
        return Token.objects.get(user=obj).key
