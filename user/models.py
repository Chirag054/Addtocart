from datetime import datetime
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from cart.models import Cart


class UserAuth:

    def email_is_used(self, email: str) -> bool:
        if email is not None:
            return User.objects.filter(email=email).exists()
        return False

    def create_new_user(self, data: object) -> User:
        new_user = User.objects.create_user(data.get('username'), data.get('email'), data.get('password'))
        new_user.first_name = data.get('first_name')
        new_user.last_name = data.get('last_name')
        new_user.last_login = datetime.now(tz=pytz.utc)
        new_user.save()
        return new_user

    def get_token(self, user):
        return Token.objects.get_or_create(user=user)

    @transaction.atomic()
    def prepare_new_user(self, data):
        email = data.get('email', None)
        if not self.email_is_used(email):
            new_user = self.create_new_user(data)
            Cart().create_cart_to_new_user(new_user)
            user = authenticate(username=data.get('username'), password=data.get('password'))
            self.get_token(user)
            return new_user
        raise serializers.ValidationError({'email_used': _('This email is already used.')})

    def do_login(self, request, data):
        try:
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None and user.is_active:
                login(request, user)
                self.get_token(user)
                return user
        except User.DoesNotExist:
            raise serializers.ValidationError({'login_error': _('Email or password wrong.')})

