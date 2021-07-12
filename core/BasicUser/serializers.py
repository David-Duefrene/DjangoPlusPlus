"""Serializers for the Basic User module."""
# Django imports
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder

# Django REST imports
from rest_framework.serializers import ModelSerializer, Serializer, \
    CharField, ValidationError, EmailField

# Project imports
from .models import BasicUser
from .forms import SetBasicUserPassword

User = get_user_model()


class BasicUserSerializer(ModelSerializer):
    """Serializer for showing a basic user's data.

    Meta:
        Model: BasicUser
        Fields: username, email, first_name, last_name, get_absolute_url
    """

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
    """Serializer for editing a basic user's data.

    Meta:
        Model: BasicUser
        Fields: email, first_name, last_name
    """

    class Meta:
        """The Meta

        Attributes:
            Model: BasicUser
            Fields: email, first_name, last_name
        """

        model = BasicUser
        fields = ['email', 'first_name', 'last_name']


class RegisterSerializer(ModelSerializer):
    """Serializer to register a basic user.

    Meta:
        Model: BasicUser
        Fields: username, email, password, first_name, last_name
        extra_kwargs = {'password': {'write_only': True}}
    """

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

    Methods:
        validate(data): Validates the user's username and password, double
            checks to make sure user is active.
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


class PasswordResetSerializer(Serializer):
    """Serializer for requesting a password reset e-mail.

    Attributes:
        email: set to EmailField
        password_reset_form_class: Set to
        reset_form: the reset form the user has filled out

    Methods:
        validate_email(self, value):
        save(self):
    """

    email = EmailField()
    password_reset_form_class = PasswordResetForm
    reset_form = None

    def validate_email(self, value):
        """Validate the email address that was entered."""
        self.reset_form = self.password_reset_form_class(data=self.initial_data)  # noqa: E501
        if not self.reset_form.is_valid():
            raise ValidationError(self.reset_form.errors)
        return value

    def save(self):
        """Save the form."""
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            # 'html_email_template_name': 'password/password_reset_email.html',
            'request': request,
        }

        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(Serializer):
    """Serializer for confirming a password reset attempt.

    Attributes:
        new_password: the new password the user is setting
        uid: unique ID to get the user
        token: the token that was generated for the password reset URL
        set_password_form_class: sets SetPasswordForm by default
        set_password_form: the form the user is filling out
    """

    new_password = CharField(max_length=128)
    uid = CharField()
    token = CharField()
    set_password_form_class = SetBasicUserPassword
    # user = None
    set_password_form = None

    class Meta:
        """The Meta"""

        fields = ['new_password', 'uid', 'token']

    def validate(self, attrs):
        """Validate the form to set new password."""
        user = None
        # Decode the uidb64 to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        # Check the token
        if not default_token_generator.check_token(user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.set_password_form = self.set_password_form_class(
            user=user, data=attrs,
        )
        # Make sure password is valid
        if not self.set_password_form.is_valid():
            raise ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        """Save the new password."""
        self.validate(attrs=self.data)
        return self.set_password_form.save(self.data)
