"""Serializers for the Basic User module."""
from django.contrib.auth import authenticate, get_user_model

from rest_framework.serializers import ModelSerializer, Serializer, \
    CharField, ValidationError

from .models import BasicUser

User = get_user_model()


class BasicUserSerializer(ModelSerializer):
    """Serializer for showing a basic user's data."""

    class Meta:
        """The Meta

        Attributes:
            Model: BasicUser
            Fields: username, email, first_name, last_name, get_absolute_url
        """

        model = BasicUser
        fields = ['username', 'email', 'first_name', 'last_name',
                  'get_absolute_url']


class EditSerializer(ModelSerializer):
    """Serializer for editing a basic user's data."""

    class Meta:
        """The Meta

        Attributes:
            Model: BasicUser
            Fields: email, first_name, last_name
        """

        model = BasicUser
        fields = ['email', 'first_name', 'last_name']


class RegisterSerializer(ModelSerializer):
    """Serializer to register a basic user."""

    class Meta:
        """The Meta

        Attributes:
            Model: BasicUser
            Fields: username, email, password, first_name, last_name
            extra_kwargs = {'password': {'write_only': True}}
        """

        model = BasicUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(Serializer):
    """Serializer to log a basic user in.

    Attributes:
        username(CharField): The user's username
        password(CharField): The user's password
    """

    username = CharField()
    password = CharField()

    @staticmethod
    def validate(data):
        """Validate the user data"""
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise ValidationError("Incorrect Credentials")


class ChangePasswordSerializer(Serializer):
    """Serializer for password change.

    Attributes:
        model: BasicUser
        old_password(CharField): The user's old password
        new_password(CharField): The user's new password
    """

    model = BasicUser
    old_password = CharField(required=True)
    new_password = CharField(required=True)
