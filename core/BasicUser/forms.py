"""Contains forms for creating and editing a basic user."""
from django.contrib.auth.forms import UserCreationForm
# from django.forms import Form, CharField
from django.contrib.auth import get_user_model


class CreateBasicUserForm(UserCreationForm):
    """Form to create a basic user."""

    class Meta:
        """The Meta

        Attributes:
            model: The user model set in settings.py
            fields: A list of fields the user contains
        """

        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2')
